from ..utils import thirty_days_ago, today
from sqlalchemy import func
from timeseries_metric import TimeseriesMetric
from form_fields import CommaSeparatedIntegerListField, BetterDateTimeField
from wtforms.validators import Required
from wikimetrics.models import Page, Revision


__all__ = ['PagesCreated']


class PagesCreated(TimeseriesMetric):
    """
    This class counts the pages created by editors over a period of time.

    This sql query was used as a starting point for the sqlalchemy query:

    SELECT count(*)
    FROM <database>.revision
    JOIN <database>.page
        ON rev_page = page_id
    WHERE rev_parent_id = 0
        AND <where>
        AND rev_user = %(user)s
        AND rev_timestamp > %(start)s
        AND rev_timestamp <= %(end)s
    """
    
    show_in_ui  = True
    id          = 'pages_created'
    label       = 'Pages Created'
    description = (
        'Compute the number of pages created by each \
         editor in a time interval'
    )
    
    namespaces = CommaSeparatedIntegerListField(
        None,
        [Required()],
        default='0',
        description='0, 2, 4, etc.',
    )
    
    def __call__(self, user_ids, session):
        """
        Parameters:
            user_ids    : list of mediawiki user ids to find edit for
            session     : sqlalchemy session open on a mediawiki database
        
        Returns:
            dictionary from user ids to the number of edit found.
        """
        # TODO: (low-priority) take into account cases where rev_deleted = 1
        start_date = self.start_date.data
        end_date = self.end_date.data
        
        pages_by_user = session\
            .query(Revision.rev_user, func.count(Page.page_id))\
            .join(Page)\
            .filter(Page.page_namespace.in_(self.namespaces.data))\
            .filter(Revision.rev_parent_id == 0)\
            .filter(Revision.rev_user.in_(user_ids))\
            .filter(Revision.rev_timestamp > start_date)\
            .filter(Revision.rev_timestamp <= end_date)\
            .group_by(Revision.rev_user)
        
        query = self.apply_timeseries(pages_by_user)
        return self.results_by_user(
            user_ids,
            query,
            [('pages_created', 1, 0)],
            date_index=2,
        )
