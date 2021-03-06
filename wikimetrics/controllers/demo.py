from flask import render_template, redirect, request, jsonify
from flask.ext.login import current_user
from sqlalchemy import func

from ..configurables import app, db
from ..models import (
    WikiUser,
    User,
    MediawikiUser,
    Cohort,
    CohortUser,
    CohortUserRole,
    CohortWikiUser,
    MetricReport,
)
from ..models.mediawiki import Revision, Page
from datetime import datetime
from ..metrics import RandomMetric


if app.config['DEBUG']:
    def delete_my_cohorts(db_sess):
        user = db_sess.query(User).filter_by(email=current_user.email).one()
        
        # delete all of this user's data
        cohort_users = db_sess.query(CohortUser).filter_by(user_id=user.id)
        cohort_users.delete()
        cwu = db_sess.query(CohortWikiUser)\
            .join(Cohort)\
            .join(CohortUser)\
            .filter(CohortUser.user_id == user.id)\
            .all()
        wu = db_sess.query(WikiUser)\
            .join(CohortWikiUser)\
            .join(Cohort)\
            .join(CohortUser)\
            .filter(CohortUser.user_id == user.id)\
            .all()
        c = db_sess.query(Cohort)\
            .join(CohortUser)\
            .filter(CohortUser.user_id == user.id)\
            .filter(CohortUser.role == CohortUserRole.OWNER)\
            .all()
        
        db_sess.commit()
        
        for r in cwu:
            db_sess.delete(r)
        for r in wu:
            db_sess.delete(r)
        for r in c:
            db_sess.delete(r)
        
        db_sess.commit()
        return user
    
    @app.route('/demo/metric/random/<int:cohort_id>')
    def run_task_in_celery(cohort_id):
        db_session = db.get_session()
        try:
            user_ids = db_session.query(WikiUser.mediawiki_userid)\
                .join(CohortWikiUser)\
                .filter(CohortWikiUser.cohort_id == cohort_id)\
                .all()
            if len(user_ids) == 0:
                user_ids = db_session.query(WikiUser.mediawiki_userid).all()
        finally:
            db_session.close()
        # note that this code runs only in development
        # TODO, what about working with more than one project in development?
        # need to translate from project to dbName
        report = MetricReport(RandomMetric(), user_ids, 'wiki')
        #from nose.tools import set_trace; set_trace()
        res = report.task.delay(report).get()
        return str(res)
    
    @app.route('/demo/delete/cohorts/')
    def demo_delete_cohorts():
        db_sess = db.get_session()
        delete_my_cohorts(db_sess)
        db_sess.close()
        return 'OK, wiped out the database only for ' + current_user.email
    
    @app.route('/demo/create/cohorts/')
    def demo_add_cohorts():
        db_sess = db.get_session()
        user = delete_my_cohorts(db_sess)
        
        # add cohorts and assign ownership to the passed-in user
        cohort1 = Cohort(name='Algeria Summer Teahouse', description='', enabled=True)
        cohort2 = Cohort(name='Berlin Beekeeping Society', description='', enabled=True)
        cohort3 = Cohort(name='A/B April', description='', enabled=True)
        cohort4 = Cohort(name='A/B March', description='', enabled=True)
        cohort5 = Cohort(name='A/B February', description='', enabled=True)
        cohort6 = Cohort(name='A/B January', description='', enabled=True)
        cohort7 = Cohort(name='A/B December', description='', enabled=True)
        cohort8 = Cohort(name='A/B October', description='', enabled=True)
        cohort9 = Cohort(name='A/B September', description='', enabled=True)
        cohort10 = Cohort(name='A/B August', description='', enabled=True)
        cohort11 = Cohort(name='A/B July', description='', enabled=True)
        cohorts = [
            cohort1, cohort2, cohort3, cohort4, cohort5, cohort6,
            cohort7, cohort8, cohort9, cohort10, cohort11
        ]
        mark_cohorts_validated(cohorts)
        db_sess.add_all(cohorts)
        db_sess.commit()
        
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort1.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort2.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort3.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort4.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort5.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort6.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort7.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort8.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort9.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort10.id, role=CohortUserRole.OWNER)
        )
        db_sess.add(
            CohortUser(user_id=user.id, cohort_id=cohort11.id, role=CohortUserRole.OWNER)
        )
        
        # TODO: these users don't actually exist in the mediawiki databases, add them
        wu1 = WikiUser(mediawiki_username='Dan', mediawiki_userid=1, project='wiki')
        wu2 = WikiUser(mediawiki_username='Evan', mediawiki_userid=2, project='wiki')
        wu3 = WikiUser(mediawiki_username='Andrew', mediawiki_userid=3, project='wiki')
        wu4 = WikiUser(
            mediawiki_username='Diederik', mediawiki_userid=4, project='wiki'
        )
        
        wu5 = WikiUser(mediawiki_username='Andrea', mediawiki_userid=5, project='dewiki')
        wu6 = WikiUser(mediawiki_username='Dennis', mediawiki_userid=6, project='dewiki')
        wu7 = WikiUser(mediawiki_username='Florian', mediawiki_userid=7, project='dewiki')
        wu8 = WikiUser(
            mediawiki_username='Gabriele', mediawiki_userid=8, project='dewiki'
        )
        
        wu9 = WikiUser(mediawiki_username='n/a', mediawiki_userid=9, project='wiki')
        wu10 = WikiUser(mediawiki_username='n/a', mediawiki_userid=10, project='wiki')
        wu11 = WikiUser(mediawiki_username='n/a', mediawiki_userid=11, project='wiki')
        
        wu12 = WikiUser(mediawiki_username='n/a', mediawiki_userid=12, project='wiki')
        wu13 = WikiUser(mediawiki_username='n/a', mediawiki_userid=13, project='wiki')
        wu14 = WikiUser(mediawiki_username='n/a', mediawiki_userid=14, project='wiki')
        
        wu15 = WikiUser(mediawiki_username='n/a', mediawiki_userid=15, project='wiki')
        wu16 = WikiUser(mediawiki_username='n/a', mediawiki_userid=16, project='wiki')
        wu17 = WikiUser(mediawiki_username='n/a', mediawiki_userid=17, project='wiki')
        
        wu18 = WikiUser(mediawiki_username='n/a', mediawiki_userid=18, project='wiki')
        wu19 = WikiUser(mediawiki_username='n/a', mediawiki_userid=19, project='wiki')
        wu20 = WikiUser(mediawiki_username='n/a', mediawiki_userid=20, project='wiki')
        
        wu21 = WikiUser(mediawiki_username='n/a', mediawiki_userid=21, project='wiki')
        wu22 = WikiUser(mediawiki_username='n/a', mediawiki_userid=22, project='wiki')
        wu23 = WikiUser(mediawiki_username='n/a', mediawiki_userid=23, project='wiki')
        
        wu24 = WikiUser(mediawiki_username='n/a', mediawiki_userid=24, project='wiki')
        wu25 = WikiUser(mediawiki_username='n/a', mediawiki_userid=25, project='wiki')
        wu26 = WikiUser(mediawiki_username='n/a', mediawiki_userid=26, project='wiki')
        
        wu27 = WikiUser(mediawiki_username='n/a', mediawiki_userid=27, project='wiki')
        wu28 = WikiUser(mediawiki_username='n/a', mediawiki_userid=28, project='wiki')
        wu29 = WikiUser(mediawiki_username='n/a', mediawiki_userid=29, project='wiki')
        
        wu30 = WikiUser(mediawiki_username='n/a', mediawiki_userid=30, project='wiki')
        wu31 = WikiUser(mediawiki_username='n/a', mediawiki_userid=31, project='wiki')
        wu32 = WikiUser(mediawiki_username='n/a', mediawiki_userid=32, project='wiki')
        
        wu33 = WikiUser(mediawiki_username='n/a', mediawiki_userid=33, project='wiki')
        wu34 = WikiUser(mediawiki_username='n/a', mediawiki_userid=34, project='wiki')
        wu35 = WikiUser(mediawiki_username='n/a', mediawiki_userid=35, project='wiki')
        
        db_sess.add_all([
            wu1, wu2, wu3, wu4, wu5, wu6, wu7, wu8, wu9, wu10, wu11, wu12,
            wu13, wu14, wu15, wu16, wu17, wu18, wu19, wu20, wu21, wu22, wu23,
            wu24, wu25, wu26, wu27, wu28, wu29, wu30, wu31, wu32, wu33, wu34,
            wu35,
        ])
        db_sess.commit()
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu1.id, cohort_id=cohort1.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu2.id, cohort_id=cohort1.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu3.id, cohort_id=cohort1.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu4.id, cohort_id=cohort1.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu5.id, cohort_id=cohort2.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu6.id, cohort_id=cohort2.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu7.id, cohort_id=cohort2.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu8.id, cohort_id=cohort2.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu9.id, cohort_id=cohort3.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu10.id, cohort_id=cohort3.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu11.id, cohort_id=cohort3.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu12.id, cohort_id=cohort4.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu13.id, cohort_id=cohort4.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu14.id, cohort_id=cohort4.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu15.id, cohort_id=cohort5.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu16.id, cohort_id=cohort5.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu17.id, cohort_id=cohort5.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu18.id, cohort_id=cohort6.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu19.id, cohort_id=cohort6.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu20.id, cohort_id=cohort6.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu21.id, cohort_id=cohort7.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu22.id, cohort_id=cohort7.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu23.id, cohort_id=cohort7.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu24.id, cohort_id=cohort8.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu25.id, cohort_id=cohort8.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu26.id, cohort_id=cohort8.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu27.id, cohort_id=cohort9.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu28.id, cohort_id=cohort9.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu29.id, cohort_id=cohort9.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu30.id, cohort_id=cohort10.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu31.id, cohort_id=cohort10.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu32.id, cohort_id=cohort10.id))
        
        db_sess.add(CohortWikiUser(wiki_user_id=wu33.id, cohort_id=cohort11.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu34.id, cohort_id=cohort11.id))
        db_sess.add(CohortWikiUser(wiki_user_id=wu35.id, cohort_id=cohort11.id))
        
        db_sess.commit()
        db_sess.close()
        
        return 'OK, wiped out the database and added cohorts only for {0}'.format(
            current_user.email
        )
    
    @app.route('/demo/create/fake-<string:project>-users/<int:n>')
    def add_fake_wiki_users(project, n):
        session = db.get_mw_session(project)
        try:
            max_id = session.query(func.max(MediawikiUser.user_id)).one()[0] or 0
            start = max_id + 1
            session.bind.engine.execute(
                MediawikiUser.__table__.insert(),
                [
                    {
                        'user_name'         : 'user-{0}'.format(r),
                        'user_id'           : r,
                        'user_registration' : '20130101000000'
                    }
                    for r in range(start, start + n)
                ]
            )
            session.commit()
        finally:
            session.close()
        return '{0} user records created in {1}'.format(n, project)


def mark_cohorts_validated(cohorts):
    for c in cohorts:
        c.validated = True
