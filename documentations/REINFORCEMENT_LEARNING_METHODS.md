# Reinforcement Learning Methods Documentation

## Overview

The Soil Health & Crop Recommendation System implements a Reinforcement Learning (RL) model using Q-Learning to provide intelligent crop recommendations. Unlike traditional machine learning models that are static after training, this RL model continuously learns and improves from farmer feedback, making it adaptive to real-world conditions.

## Architecture

### Q-Learning Approach

The RL model uses Q-Learning, a model-free reinforcement learning algorithm that learns a policy telling an agent what action to take under what circumstances. In our case:

- **States**: Environmental conditions (soil nutrients, weather, soil type)
- **Actions**: Crop recommendations
- **Rewards**: Farmer feedback on recommendation success

### State Representation

States are discretized based on environmental features:
- Nitrogen (N): Binned in 20 mg/kg intervals
- Phosphorus (P): Binned in 20 mg/kg intervals
- Potassium (K): Binned in 20 mg/kg intervals
- Temperature: Binned in 5°C intervals
- Rainfall: Binned in 200mm intervals
- pH: Binned in 0.5 unit intervals
- Soil Type: Encoded categorical variable

State key format: `{N_bin}_{P_bin}_{K_bin}_{temp_bin}_{rain_bin}_{ph_bin}_{soil_type}`

### Action Space

The action space consists of 20 crops commonly grown in North Karnataka:
- bajra, blackgram, chickpea, chilli, cotton, grapes, greengram
- groundnut, jowar, lentil, maize, onion, pigeonpeas, pomegranate
- ragi, safflower, soybean, sugarcane, sunflower, tomato, wheat

### Reward System

Rewards are assigned based on farmer feedback:
- **+1.0**: Perfect match - recommended crop matches actual crop and was successful
- **+0.5**: Partial success - farmer chose different crop but it was successful
- **-1.0**: Failure - recommendation was unsuccessful
- **-0.5**: Pre-training penalty - incorrect predictions during initial training

## Implementation Details

### Core Class: CropRecommendationRL

Located in `app/main.py`, this class implements the Q-Learning algorithm:

```python
class CropRecommendationRL:
    def __init__(self, crops, learning_rate=0.1, discount_factor=0.95, epsilon=0.2):
        self.crops = crops
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = {}
        self.experience_buffer = []
```

### Key Methods

1. **predict(features)**: Returns crop recommendation and confidence
2. **get_top_recommendations(features, top_n=3)**: Returns top N crop recommendations with confidence scores
3. **update(features, recommended_crop, actual_crop, reward)**: Updates Q-table based on feedback
4. **get_stats()**: Returns model statistics

### Exploration vs Exploitation

The model uses ε-greedy strategy:
- With probability ε (0.2): Random exploration
- With probability 1-ε (0.8): Exploit learned knowledge

### Experience Replay

The model maintains an experience buffer of size 10,000 to:
- Store past experiences for learning
- Prevent catastrophic forgetting
- Enable learning from historical feedback

## Training Process

### Initial Training

The model is pre-trained using the North Karnataka dataset:
1. Dataset is split into training (80%) and testing (20%)
2. Model simulates farmer feedback using actual crop labels
3. Q-table is populated through simulated interactions

### Continuous Learning

The model continuously improves through:
1. Farmer feedback via the RL feedback endpoint
2. Real-world results from crop implementations
3. Experience replay from historical feedback

## API Endpoints

### GET /models

Returns information about available models including the RL model.

### POST /rl-feedback

Accepts farmer feedback to improve the model:

**Required Fields:**
- N, P, K: Soil nutrient levels
- temperature, humidity, ph, rainfall: Environmental conditions
- soil_type: Type of soil
- recommended_crop: Crop that was recommended
- actual_crop: Crop that was actually planted
- success: Boolean indicating if the recommendation was successful

**Response:**
- Reward value assigned
- Updated model statistics
- Success confirmation

## Model Performance

### Current Statistics

Based on the latest training metadata:
- Training samples: 11,760
- Test samples: 2,940
- Test accuracy: ~3.67%
- States explored: 4,798
- Experience buffer size: 10,000

### Hyperparameters

- Learning rate (α): 0.1
- Discount factor (γ): 0.95
- Exploration rate (ε): 0.2

## Integration with Main System

The RL model is integrated as one of the available prediction models:
1. Available through the standard `/predict` endpoint
2. Selectable via the `model_name` parameter
3. Can be used alongside ensemble methods

## Future Improvements

1. **Advanced Reward Functions**: Incorporate yield data, market prices, and profit margins
2. **Multi-step Learning**: Consider crop rotation and seasonal effects
3. **Transfer Learning**: Adapt to different regions with limited data
4. **Uncertainty Quantification**: Better confidence estimates for recommendations
5. **Federated Learning**: Learn from multiple farms while preserving privacy

## Usage Guidelines

### For Farmers

1. Use the RL model when you want adaptive recommendations
2. Provide feedback on successful and unsuccessful recommendations
3. The model improves with each feedback submission

### For Developers

1. The model is loaded automatically with other ML models
2. Feedback is processed through the `/rl-feedback` endpoint
3. Model updates are automatically saved to disk
4. Monitor model statistics through the `/model-stats` endpoint

## Technical Considerations

### Scalability

- Q-table grows with state exploration
- Memory usage is bounded by experience buffer (10,000 entries)
- State discretization balances accuracy with memory efficiency

### Robustness

- Handles missing states through random initialization
- Experience replay prevents overfitting to recent feedback
- Epsilon-greedy ensures continued exploration

### Maintenance

- Model is automatically saved after each feedback
- Metadata tracking enables performance monitoring
- Easy to retrain with updated datasets

## Conclusion

The Reinforcement Learning model represents a significant advancement in agricultural AI by enabling continuous learning from real-world results. This approach addresses the limitations of static models and adapts to changing environmental conditions, making crop recommendations increasingly accurate over time.