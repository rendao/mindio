import json
from typing import Dict, Any, Optional

class ToolRegistry:
    """Registry for available tools"""
    
    def __init__(self, knowledge_base=None):
        self.knowledge_base = knowledge_base
        self.tools = {
            "symptom_search": self.symptom_search,
            "assessment_tool": self.assessment_tool,
            "coping_strategies": self.coping_strategies
        }
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name with the provided parameters"""
        if tool_name not in self.tools:
            return {
                "status": "error",
                "message": f"Tool '{tool_name}' not found",
                "result": None
            }
            
        try:
            result = self.tools[tool_name](**parameters)
            return {
                "status": "success",
                "message": "Tool executed successfully",
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error executing tool: {str(e)}",
                "result": None
            }
    
    def symptom_search(self, symptom: str) -> Dict[str, Any]:
        """Search for information about mental health symptoms"""
        if self.knowledge_base:
            # Search the knowledge base for relevant information
            results = self.knowledge_base.search(symptom, top_k=2)
            
            if results:
                return {
                    "found": True,
                    "information": [doc['content'] for doc in results],
                    "count": len(results)
                }
        
        # Default response if no knowledge base or no results
        return {
            "found": False,
            "information": ["No specific information found for this symptom."],
            "count": 0
        }
    
    def assessment_tool(self, assessment_type: str) -> Dict[str, Any]:
        """Provide a standardized psychological assessment"""
        assessments = {
            "anxiety": {
                "name": "GAD-7 (Generalized Anxiety Disorder Assessment)",
                "description": "A 7-item questionnaire used as a screening tool and severity measure for generalized anxiety disorder.",
                "questions": [
                    "Feeling nervous, anxious, or on edge",
                    "Not being able to stop or control worrying",
                    "Worrying too much about different things",
                    "Trouble relaxing",
                    "Being so restless that it's hard to sit still",
                    "Becoming easily annoyed or irritable",
                    "Feeling afraid as if something awful might happen"
                ],
                "scoring": "Rate each item from 0 (Not at all) to 3 (Nearly every day). Scores of 5, 10, and 15 are cut-points for mild, moderate, and severe anxiety."
            },
            "depression": {
                "name": "PHQ-9 (Patient Health Questionnaire)",
                "description": "A 9-item questionnaire used as a screening tool and severity measure for depression.(A thoughtful, personalized follow-up question or a transition to the analysis phase.)",
                "questions": [
                    "Little interest or pleasure in doing things",
                    "Feeling down, depressed, or hopeless",
                    "Trouble falling or staying asleep, or sleeping too much",
                    "Feeling tired or having little energy",
                    "Poor appetite or overeating",
                    "Feeling bad about yourself or that you are a failure",
                    "Trouble concentrating on things",
                    "Moving or speaking slowly, or being fidgety/restless",
                    "Thoughts that you would be better off dead or of hurting yourself"
                ],
                "scoring": "Rate each item from 0 (Not at all) to 3 (Nearly every day). Scores of 5, 10, 15, and 20 are cut-points for mild, moderate, moderately severe, and severe depression."
            },
            "stress": {
                "name": "PSS-10 (Perceived Stress Scale)",
                "description": "A 10-item questionnaire that measures the perception of stress.",
                "questions": [
                    "Been upset because of something that happened unexpectedly",
                    "Felt unable to control important things in your life",
                    "Felt nervous and stressed",
                    "Felt confident about your ability to handle personal problems",
                    "Felt that things were going your way",
                    "Found that you could not cope with all the things you had to do",
                    "Been able to control irritations in your life",
                    "Felt that you were on top of things",
                    "Been angered because of things that happened that were outside of your control",
                    "Felt difficulties were piling up so high that you could not overcome them"
                ],
                "scoring": "Items are rated on a 5-point scale from 0 (Never) to 4 (Very often). Positively worded items are reverse-scored, and the scores are summed. Higher scores indicate higher levels of perceived stress."
            }
        }
        
        if assessment_type in assessments:
            return {
                "assessment_info": assessments[assessment_type],
                "guidance": "The assistant should conduct this assessment by asking only one question at a time. Wait for the user's response before proceeding to the next question. After all questions are answered, provide a thoughtful analysis of the results without presenting numerical scores. Focus on identifying patterns in the responses and offering relevant suggestions."
            }
    
        return {
            "name": "Unknown assessment",
            "description": "The requested assessment type is not available.",
            "guidance": "Please inform the user that this assessment is not available and suggest alternatives."
        }
    
    def coping_strategies(self, challenge: str) -> Dict[str, Any]:
        """Suggest evidence-based coping strategies"""
        # Dictionary of coping strategies for common challenges
        strategies = {
            "anxiety": [
                {
                    "name": "Deep Breathing",
                    "description": "Practice deep breathing by inhaling slowly through your nose for 4 counts, holding for 2 counts, and exhaling through your mouth for 6 counts. Repeat for 5-10 minutes."
                },
                {
                    "name": "Progressive Muscle Relaxation",
                    "description": "Tense and then release each muscle group in your body, starting from your toes and working up to your head."
                },
                {
                    "name": "Grounding Technique",
                    "description": "Use the 5-4-3-2-1 technique: Acknowledge 5 things you see, 4 things you can touch, 3 things you hear, 2 things you smell, and 1 thing you taste."
                }
            ],
            "depression": [
                {
                    "name": "Behavioral Activation",
                    "description": "Schedule and engage in activities that you used to enjoy, even if you don't feel like it initially."
                },
                {
                    "name": "Physical Exercise",
                    "description": "Aim for 30 minutes of moderate exercise most days of the week. Even a short walk can help improve mood."
                },
                {
                    "name": "Social Connection",
                    "description": "Reach out to supportive friends or family members, even briefly. Social interaction can help combat feelings of isolation."
                }
            ],
            "stress": [
                {
                    "name": "Mindfulness Meditation",
                    "description": "Practice focusing on the present moment without judgment. Start with just 5 minutes daily."
                },
                {
                    "name": "Time Management",
                    "description": "Break larger tasks into smaller, manageable steps. Prioritize tasks and consider using the Pomodoro technique (25 minutes of focus followed by a 5-minute break)."
                },
                {
                    "name": "Healthy Boundaries",
                    "description": "Practice saying no to additional commitments when you're already stretched thin."
                }
            ]
        }
        
        # Search for the challenge in our strategies dictionary
        # Do a simple keyword matching for relevant strategies
        results = []
        for key, strats in strategies.items():
            if key in challenge.lower() or challenge.lower() in key:
                results.extend(strats)
        
        # If no direct match, provide general strategies
        if not results:
            results = [
                {
                    "name": "Self-Care",
                    "description": "Ensure you're attending to basic needs: adequate sleep, nutritious food, hydration, and some physical activity."
                },
                {
                    "name": "Journaling",
                    "description": "Write about your feelings and experiences for 10-15 minutes to help process emotions."
                },
                {
                    "name": "Professional Support",
                    "description": "Consider speaking with a mental health professional who can provide personalized guidance."
                }
            ]
        
        return {
            "challenge": challenge,
            "strategies": results
        }