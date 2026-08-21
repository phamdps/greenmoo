import mlflow
import time
import pickle
import os
from functools import wraps

def track_green_experiment(experiment_name="GreenMOO-Optimization"):
    """
    Decorator to wrap GreenMOO optimization runs with MLflow tracking,
    logging parameters, execution duration, carbon metrics, 
    and serializing the resulting Pareto front population as an artifact.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mlflow.set_experiment(experiment_name)
            with mlflow.start_run():
                alg_name = kwargs.get("algorithm_name", "NSGAII")
                prob_name = kwargs.get("problem_name", "DTLZ2")
                
                mlflow.log_param("algorithm", alg_name)
                mlflow.log_param("problem", prob_name)
                
                for k, v in kwargs.items():
                    if k not in ["algorithm_name", "problem_name"]:
                        mlflow.log_param(k, v)
                
                start_time = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Proxy or calculated green metrics
                energy_kwh = duration * 0.000045  
                carbon_g = energy_kwh * 475.0  # gCO2eq
                
                mlflow.log_metric("duration_seconds", duration)
                mlflow.log_metric("energy_consumption_kwh", energy_kwh)
                mlflow.log_metric("carbon_footprint_gco2", carbon_g)
                
                if result and hasattr(result, "result"):
                    mlflow.log_metric("pareto_front_size", len(result.result))
                    
                    # Save Pareto front population as an artifact for later visualization
                    artifact_file = "pareto_solutions.pkl"
                    with open(artifact_file, "wb") as f:
                        pickle.dump(result.result, f)
                    
                    mlflow.log_artifact(artifact_file)
                    if os.path.exists(artifact_file):
                        os.remove(artifact_file)  # Clean up local temp file
                
                return result
        return wrapper
    return decorator