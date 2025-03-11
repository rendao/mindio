from typing import List, Dict, Any

# an example of a function that analyzes the emotional content of a user input
# and returns a summary of the detected emotions
# TODO 
def analyze_emotional_content(user_input: str) -> Dict[str, Any]:
    positive_emotions = ["开心", "快乐", "满足", "放松", "喜悦", "希望"]
    negative_emotions = ["焦虑", "压力", "伤心", "难过", "失望", "痛苦", "愤怒", "恐惧"]
    neutral_emotions = ["困惑", "迷茫", "不确定", "平静", "一般"]

    emotional_analysis = {
        "positive": [],
        "negative": [],
        "neutral": []
    }

    for word in user_input.split():
        if word in positive_emotions:
            emotional_analysis["positive"].append(word)
        elif word in negative_emotions:
            emotional_analysis["negative"].append(word)
        elif word in neutral_emotions:
            emotional_analysis["neutral"].append(word)

    return emotional_analysis

def summarize_emotional_analysis(emotional_analysis: Dict[str, Any]) -> str:
    summary_parts = []
    
    if emotional_analysis["positive"]:
        summary_parts.append(f"积极情绪: {', '.join(emotional_analysis['positive'])}")
    if emotional_analysis["negative"]:
        summary_parts.append(f"消极情绪: {', '.join(emotional_analysis['negative'])}")
    if emotional_analysis["neutral"]:
        summary_parts.append(f"中性情绪: {', '.join(emotional_analysis['neutral'])}")

    return " | ".join(summary_parts) if summary_parts else "未检测到情绪。"

def main(user_input: str) -> str:
    emotional_analysis = analyze_emotional_content(user_input)
    return summarize_emotional_analysis(emotional_analysis)