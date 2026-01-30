#Viability scoring (0-100)

"""
Scoring Module - Reuse Viability Scoring & Verdict System
Calculates final reuse scores and generates user-friendly verdicts
"""

from typing import Dict, Tuple


def calculate_reuse_score(analysis: Dict) -> int:
    """
    Calculate final reuse viability score (0-100)
    
    Combines confidence from LLM with condition factors
    
    Args:
        analysis: Analysis output from reasoning module
        
    Returns:
        Integer score from 0-100
    """
    base_confidence = analysis.get("confidence", 50)
    
    # Adjust based on verdict
    verdict = analysis.get("verdict", "Unknown")
    
    if verdict == "Not Reusable":
        # Cap at 30 for non-reusable items
        return min(int(base_confidence), 30)
    elif verdict == "Conditionally Reusable":
        # Range 40-75 for conditional
        return max(40, min(int(base_confidence), 75))
    elif verdict == "Reusable":
        # Range 60-100 for reusable
        return max(60, min(int(base_confidence), 100))
    else:
        return int(base_confidence)


def get_verdict_display(verdict: str, score: int) -> Dict[str, str]:
    """
    Get display properties for verdict
    
    Args:
        verdict: Verdict string
        score: Reuse score
        
    Returns:
        Dictionary with display properties
    """
    verdict_config = {
        "Reusable": {
            "color": "green",
            "emoji": "✅",
            "message": "This object is suitable for reuse!",
            "icon": "🌱"
        },
        "Conditionally Reusable": {
            "color": "orange",
            "emoji": "⚠️",
            "message": "This object can be reused with some preparation or limitations.",
            "icon": "🔄"
        },
        "Not Reusable": {
            "color": "red",
            "emoji": "❌",
            "message": "This object is not recommended for reuse.",
            "icon": "🚫"
        },
        "Analysis Failed": {
            "color": "gray",
            "emoji": "⚠️",
            "message": "Unable to analyze this object.",
            "icon": "❓"
        }
    }
    
    return verdict_config.get(verdict, verdict_config["Analysis Failed"])


def generate_score_interpretation(score: int) -> str:
    """
    Generate human-readable interpretation of score
    
    Args:
        score: Reuse viability score
        
    Returns:
        Interpretation string
    """
    if score >= 80:
        return "Excellent reuse potential - minimal preparation needed"
    elif score >= 65:
        return "Good reuse potential - suitable for most applications"
    elif score >= 50:
        return "Moderate reuse potential - may need cleaning or minor repairs"
    elif score >= 35:
        return "Limited reuse potential - significant limitations apply"
    else:
        return "Low reuse potential - not recommended for most uses"


def format_final_output(vision_result: Dict, analysis: Dict) -> Dict:
    """
    Format complete analysis into user-friendly output
    
    Args:
        vision_result: Output from vision module
        analysis: Output from reasoning module
        
    Returns:
        Formatted final output dictionary
    """
    score = calculate_reuse_score(analysis)
    verdict = analysis.get("verdict", "Unknown")
    verdict_display = get_verdict_display(verdict, score)
    
    return {
        "object_type": vision_result.get("object_type", "Unknown"),
        "score": score,
        "score_interpretation": generate_score_interpretation(score),
        "verdict": verdict,
        "verdict_display": verdict_display,
        "condition_summary": analysis.get("condition_summary", ""),
        "visual_description": vision_result.get("description", ""),
        "reasoning": analysis.get("reasoning", ""),
        "key_factors": analysis.get("key_factors", []),
        "suggestions": analysis.get("suggestions", []),
        "reuse_feasible": analysis.get("reuse_feasible", False)
    }


def get_score_color(score: int) -> str:
    """
    Get color coding for score visualization
    
    Args:
        score: Reuse score
        
    Returns:
        Color name or hex code
    """
    if score >= 70:
        return "#28a745"  # Green
    elif score >= 50:
        return "#ffc107"  # Yellow/Orange
    elif score >= 30:
        return "#fd7e14"  # Orange
    else:
        return "#dc3545"  # Red


def generate_summary_report(final_output: Dict) -> str:
    """
    Generate a concise summary report for terminal/logging
    
    Args:
        final_output: Formatted output dictionary
        
    Returns:
        Multi-line summary string
    """
    lines = [
        "=" * 60,
        "WASTE REUSE ANALYSIS REPORT",
        "=" * 60,
        f"Object Type: {final_output['object_type']}",
        f"Reuse Score: {final_output['score']}/100",
        f"Verdict: {final_output['verdict']} {final_output['verdict_display']['emoji']}",
        "",
        "CONDITION SUMMARY:",
        final_output['condition_summary'],
        "",
        "REASONING:",
        final_output['reasoning'],
        ""
    ]
    
    if final_output['suggestions']:
        lines.append("REUSE SUGGESTIONS:")
        for i, suggestion in enumerate(final_output['suggestions'], 1):
            lines.append(f"{i}. {suggestion['use_case']}")
            lines.append(f"   → {suggestion['explanation']}")
        lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)