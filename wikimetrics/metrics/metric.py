from flask.ext import wtf
import logging
logger = logging.getLogger(__name__)

__all__ = [
    'Metric',
]


class Metric(wtf.Form):
    """
    This class is the parent of all Metric implementations.
    Child implementations should be callable and should take in users
    and return the metric computation results for each user.
    This class and its children also act as WTForms form creators by inheriting
    from wtf.Form.  It makes sure to only call the __init__ in wtf.Form when we
    are inside a flask context.
    """
    
    show_in_ui  = False
    id          = None  # unique identifier for client-side use
    label       = None  # this will be displayed as the title of the metric-specific
                        # tab in the request form
    description = None  # basic description of what the metric does
    
    def __call__(self, user_ids, session):
        """
        This is the __call__ signature any child implementations should follow.
        
        Parameters:
            user_ids    : list of mediawiki user ids to calculate the metric on
            session     : sqlalchemy session open on a mediawiki database
        
        Returns:
            dictionary from user ids to the metric results.
        """
        return {user: None for user in user_ids}
    
    def __init__(self):
        """
        This __init__ handles the problem with calling wtf.Form.__init__()
        outside of a flask request context.
        """
        try:
            wtf.Form.__init__(self)
        except(RuntimeError):
            logger.debug(
                'initializing Metric outside Flask context,'
                'most likely in testing or interactive mode'
            )
