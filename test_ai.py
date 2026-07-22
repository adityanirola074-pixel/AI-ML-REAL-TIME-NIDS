from models.predictor import predict

features = [
    6,
    1.5,
    10,
    5,
    2000,
    3000,
    10,
    1,
    8,
    64240
]

result = predict(features)

print(result)