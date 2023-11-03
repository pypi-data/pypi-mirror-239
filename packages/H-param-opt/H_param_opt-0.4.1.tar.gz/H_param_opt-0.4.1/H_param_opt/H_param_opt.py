import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import xgboost as xgb
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn import linear_model
import json

class GWOSearch:
    
    '''dict_DEFAULT_PARAMS = {
        'XGBRegressor': {
            'n_estimators': {'values': np.arange(50, 101), 'dtype': int},
            'learning_rate': {'values': np.linspace(0.01, 0.5, 50), 'dtype': float},
            'max_depth': {'values': np.arange(3, 11), 'dtype': int},
            'gamma': {'values': np.linspace(0, 0.5, 50), 'dtype': float},
            'min_child_weight': {'values': np.arange(1, 11), 'dtype': int},
            'subsample': {'values': np.linspace(0.5, 1.0, 6), 'dtype': float},
            'colsample_bytree': {'values': np.linspace(0.5, 1.0, 6), 'dtype': float},
            'reg_alpha': {'values': np.linspace(0, 1, 100), 'dtype': float}
        },
        'GradientBoostingRegressor': {
            'n_estimators': {'values': np.arange(50, 101), 'dtype': int},
            'learning_rate': {'values': np.linspace(0.01, 0.5, 50), 'dtype': float},
            'max_depth': {'values': np.arange(3, 11), 'dtype': int},
            'subsample': {'values': np.linspace(0.5, 1.0, 6), 'dtype': float},
            'min_samples_split': {'values': np.arange(2, 11), 'dtype': int},
            'min_samples_leaf': {'values': np.arange(1, 11), 'dtype': int}
        },
        'RandomForestRegressor': {
            'n_estimators': {'values': np.arange(50, 201), 'dtype': int},
            'max_depth': {'values': np.arange(3, 11), 'dtype': int},
            'min_samples_split': {'values': np.arange(2, 11), 'dtype': int},
            'min_samples_leaf': {'values': np.arange(1, 11), 'dtype': int}
        },
        'Ridge': {
            'alpha': {'values': np.linspace(0.01, 10, 100), 'dtype': float}
        }
    }'''


    def __init__(self, model, x_train, y_train, x_test, y_test, dict_params=None, population_size=20, num_iterations=50):

        self.model = model
        str_model_nm = type(self.model).__name__
        self.model_name = str_model_nm
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.population_size = population_size
        self.num_iterations = num_iterations
        
        # Load parameters from the provided JSON file
        with open("default_params.json", 'r') as f:
            self.dict_DEFAULT_PARAMS = json.load(f)
            
        for model_name, params in self.dict_DEFAULT_PARAMS.items():
            for param, details in params.items():
                if 'values' in details:
                    details['values'] = eval(details['values'])
                if 'dtype' in details:
                    details['dtype'] = eval(details['dtype'])
        #print(self.dict_DEFAULT_PARAMS)
                    
        if dict_params is not None:
            self.search_spaces = dict_params
        else:
            self.search_spaces = self.dict_DEFAULT_PARAMS.get(str_model_nm, {})
        
        # 檢查是否有超參數的搜索空間
        if not self.search_spaces:
            print("[Warning] 未提供超參數範圍，將直接使用模型預設值訓練。")
            self.population_size = 3
            self.num_iterations = 1

        self.param_types = {}  # 新建一个字典来保存参数的类型
        for key, value in self.search_spaces.items():
            self.param_types[key] = value['dtype']
            self.search_spaces[key] = value['values']


    def check_and_convert_types(self, param_name, value):
        expected_dtype = self.param_types[param_name]
        if not isinstance(value, expected_dtype):
            return expected_dtype(value)
        return value

    def create_model(self, params):
        for param_name, value in params.items():
            params[param_name] = self.check_and_convert_types(param_name, value)
        self.model.set_params(**params)
        return self.model

    def clip_population(self, population):
        for i in range(population.shape[0]):  
            for j, param_name in enumerate(self.search_spaces.keys()): 
                min_val = np.min(self.search_spaces[param_name])
                max_val = np.max(self.search_spaces[param_name])
                population[i, j] = np.clip(population[i, j], min_val, max_val)
                population[i, j] = self.check_and_convert_types(param_name, population[i, j])
        return population


    def fitness_function(self, params, target):

        model = self.create_model(params)
        model.fit(self.x_train, self.y_train.values.ravel())
        predictions = model.predict(self.x_test)

        dict_target = {
            'mape': mean_absolute_percentage_error(self.y_test, predictions) * 100,
            'rmse': np.sqrt(mean_squared_error(self.y_test, predictions)),
            'r2': -r2_score(self.y_test, predictions)
        }

        return dict_target.get(target)


    def evaluate_best_model(self, best_hyperparameters):
    
        model = self.create_model(best_hyperparameters)
        model.fit(self.x_train, self.y_train.values.ravel())
        predictions = model.predict(self.x_test)

        mape = mean_absolute_percentage_error(self.y_test, predictions) * 100
        rmse = np.sqrt(mean_squared_error(self.y_test, predictions))
        r2 = r2_score(self.y_test, predictions)

        return mape, rmse, r2


    def optimize(self, target):
        num_params = len(self.search_spaces)
        population = np.zeros((self.population_size, num_params))

        for i in range(self.population_size):
            for j, param_name in enumerate(self.search_spaces.keys()):
                population[i, j] = np.random.choice(self.search_spaces[param_name])

        best_hyperparameters = None
        best_score = float('inf')
        for iteration in range(self.num_iterations):
            
            print(f"This is {iteration+1} iteration")
            
            fitness = [self.fitness_function({key: wolf[idx] for idx, key in enumerate(self.search_spaces.keys())}, target) for wolf in population]
         
            sorted_idx = np.argsort(fitness)
            alpha = population[sorted_idx[0]]
            beta = population[sorted_idx[1]]
            delta = population[sorted_idx[2]]

            a = 2 * (1 - (iteration / self.num_iterations))

            for i in range(self.population_size):

                for j, param_name in enumerate(self.search_spaces.keys()):

                    r1, r2 = np.random.random(), np.random.random()
                    A1, C1 = 2 * a * r1 - a, 2 * r2
                    r1, r2 = np.random.random(), np.random.random()
                    A2, C2 = 2 * a * r1 - a, 2 * r2
                    r1, r2 = np.random.random(), np.random.random()
                    A3, C3 = 2 * a * r1 - a, 2 * r2

                    D_alpha = abs(C1 * alpha[j] - population[i, j])
                    D_beta = abs(C2 * beta[j] - population[i, j])
                    D_delta = abs(C3 * delta[j] - population[i, j])

                    population[i, j] = (alpha[j] - A1 * D_alpha + beta[j] - A2 * D_beta + delta[j] - A3 * D_delta) / 3

            # Clip the population values based on the search space
            population = self.clip_population(population)

            # Update the best hyperparameters if a better one is found
            if fitness[sorted_idx[0]] < best_score:

                best_score = fitness[sorted_idx[0]]
                best_hyperparameters = {key: alpha[idx] for idx, key in enumerate(self.search_spaces.keys())}
        
        return best_hyperparameters


