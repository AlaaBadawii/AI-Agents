"""Environment class"""

import traceback

from action import Action


class Environment:
    """Environment and returns structured results."""
    
    def execute_action(self, action: Action, **kwargs):
        """Execute an action and return structured results."""
        try:
            result = action.execute(**kwargs)
            return {
                "status": "success",
                "result": result,
            }    
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        
