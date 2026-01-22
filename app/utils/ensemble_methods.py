"""
Ensemble Methods for Improved Prediction Confidence
Implements soft voting, weighted ensemble, and confidence calibration
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.calibration import CalibratedClassifierCV


def soft_voting_ensemble(
    models: Dict,
    features,
    weights: Optional[Dict[str, float]] = None
) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Soft voting ensemble - combines probability predictions from multiple models
    
    Args:
        models: Dictionary of model_name -> model
        features: Input features for prediction
        weights: Optional weights for each model (default: equal weights)
    
    Returns:
        predicted_class_idx: Index of predicted class
        probabilities: Probability distribution over all classes
        confidence: Confidence score (0-100)
    """
    if weights is None:
        # Default weights based on typical model performance
        weights = {
            'Stacking Classifier': 0.25,
            'Random Forest': 0.20,
            'LightGBM': 0.20,
            'CatBoost': 0.15,
            'Gradient Boosting': 0.10,
            'XGBoost': 0.10
        }
    
    # Initialize probability array (assuming 22 crops)
    num_classes = 22
    total_proba = np.zeros(num_classes)
    total_weight = 0.0
    
    # Get predictions from each model
    for model_name, model in models.items():
        if model_name in weights:
            try:
                # Get probability predictions
                proba = model.predict_proba(features)[0]
                
                # Ensure same number of classes
                if len(proba) == num_classes:
                    weight = weights[model_name]
                    total_proba += proba * weight
                    total_weight += weight
            except Exception as e:
                print(f"⚠️ Error getting prediction from {model_name}: {e}")
                continue
    
    # Normalize probabilities
    if total_weight > 0:
        total_proba = total_proba / total_weight
    else:
        # Fallback: equal probabilities
        total_proba = np.ones(num_classes) / num_classes
    
    # Get predicted class
    predicted_class_idx = np.argmax(total_proba)
    confidence = total_proba[predicted_class_idx] * 100
    
    return predicted_class_idx, total_proba, confidence


def weighted_ensemble_predict(
    models: Dict,
    features,
    class_names: np.ndarray,
    weights: Optional[Dict[str, float]] = None
) -> Dict:
    """
    Weighted ensemble prediction with detailed results
    
    Returns:
        Dictionary with prediction, confidence, and probabilities
    """
    pred_idx, probabilities, confidence = soft_voting_ensemble(models, features, weights)
    
    # Get top 5 predictions
    top_indices = np.argsort(probabilities)[-5:][::-1]
    
    top_crops = [
        {
            "crop": class_names[idx],
            "probability": float(probabilities[idx] * 100),
            "confidence": float(probabilities[idx] * 100)
        }
        for idx in top_indices
    ]
    
    return {
        "predicted_crop": class_names[pred_idx],
        "confidence": confidence,
        "probabilities": probabilities,
        "top_crops": top_crops
    }


def adjust_confidence_by_region(
    confidence: float,
    crop: str,
    location: str,
    is_regionally_suitable: bool
) -> float:
    """
    Adjust confidence based on regional suitability
    
    Args:
        confidence: Base confidence score
        crop: Predicted crop name
        location: Location string
        is_regionally_suitable: Whether crop is suitable for region
    
    Returns:
        Adjusted confidence score
    """
    if is_regionally_suitable:
        # Boost confidence by 3-5% if regionally suitable
        boost = confidence * 0.04  # 4% boost
        return min(100.0, confidence + boost)
    else:
        # Reduce confidence by 5-10% if not suitable
        reduction = confidence * 0.08  # 8% reduction
        return max(0.0, confidence - reduction)


def calibrate_confidence(
    model,
    X_calibration,
    y_calibration
) -> object:
    """
    Calibrate model confidence using calibration set
    
    Uses Platt scaling or isotonic regression to make
    confidence scores more reliable
    """
    try:
        calibrated = CalibratedClassifierCV(
            model,
            method='isotonic',
            cv=3
        )
        calibrated.fit(X_calibration, y_calibration)
        return calibrated
    except Exception as e:
        print(f"⚠️ Calibration failed: {e}")
        return model


def get_prediction_uncertainty(
    models: Dict,
    features,
    num_samples: int = 100
) -> Dict:
    """
    Estimate prediction uncertainty using bootstrap sampling
    
    Returns uncertainty metrics for the prediction
    """
    predictions = []
    confidences = []
    
    # Get predictions from all models
    for model_name, model in models.items():
        try:
            proba = model.predict_proba(features)[0]
            pred_idx = np.argmax(proba)
            confidence = proba[pred_idx] * 100
            
            predictions.append(pred_idx)
            confidences.append(confidence)
        except:
            continue
    
    if not predictions:
        return {
            "uncertainty": 1.0,
            "agreement": 0.0,
            "std_confidence": 0.0
        }
    
    # Calculate uncertainty metrics
    agreement = len(set(predictions)) / len(predictions)  # Lower is better (more agreement)
    std_confidence = np.std(confidences) if confidences else 0.0
    
    # Uncertainty score (0-1, lower is better)
    uncertainty = (1 - agreement) * 0.5 + (std_confidence / 100) * 0.5
    
    return {
        "uncertainty": float(uncertainty),
        "agreement": float(1 - agreement),  # Higher is better
        "std_confidence": float(std_confidence),
        "num_models": len(predictions)
    }


def ensemble_with_uncertainty(
    models: Dict,
    features,
    class_names: np.ndarray,
    weights: Optional[Dict[str, float]] = None
) -> Dict:
    """
    Ensemble prediction with uncertainty quantification
    
    Returns comprehensive prediction results including uncertainty
    """
    # Get ensemble prediction
    ensemble_result = weighted_ensemble_predict(models, features, class_names, weights)
    
    # Get uncertainty metrics
    uncertainty = get_prediction_uncertainty(models, features)
    
    # Combine results
    ensemble_result.update({
        "uncertainty": uncertainty["uncertainty"],
        "model_agreement": uncertainty["agreement"],
        "confidence_std": uncertainty["std_confidence"],
        "num_models_used": uncertainty["num_models"]
    })
    
    return ensemble_result

