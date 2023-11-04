import numpy as np
import pandas as pd
from omegaconf import OmegaConf

from DBAnomTransformer.config.utils import default_config
from DBAnomTransformer.detector import DBAnomDector

dataset_name = "DBS"
# dataset_name = "EDA"

# Create config
eda_config = default_config
dbsherlock_config = OmegaConf.create(
    {
        "model": {"num_anomaly_cause": 11, "num_feature": 200},
        "model_path": "checkpoints/DBS_checkpoint.pth",
        "scaler_path": "checkpoints/DBS_scaler.pkl",
        "stats_path": "checkpoints/DBS_stats.json",
    }
)


# Create dummy data
if dataset_name == "EDA":
    feature_num = 29
elif dataset_name == "DBS":
    feature_num = 200
dummy_data = np.random.rand(130, feature_num)
dummy_data = pd.DataFrame(dummy_data, columns=[f"attr_{i}" for i in range(feature_num)])


# Initialize and train model
if dataset_name == "EDA":
    detector = DBAnomDector()
    detector.train(dataset_path="dataset/EDA2/")
elif dataset_name == "DBS":
    detector = DBAnomDector(override_config=dbsherlock_config)
    detector.train(
        dataset_path="dataset/dbsherlock/converted/tpcc_500w_test.json",
        dataset_name="DBS",
    )

# Run inference (detect anomaly)
anomaly_score, is_anomaly, anomaly_cause = detector.infer(data=dummy_data)
