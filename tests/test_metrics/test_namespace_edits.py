from nose.tools import assert_true, assert_equal
from tests.fixtures import DatabaseTest, QueueDatabaseTest

from wikimetrics.metrics import NamespaceEdits
from wikimetrics.models import Cohort, MetricReport


class NamespaceEditsDatabaseTest(DatabaseTest):
    
    def test_finds_edits(self):
        cohort = self.session.query(Cohort).filter_by(name='test').one()
        
        metric = NamespaceEdits()
        results = metric(list(cohort), self.mwSession)
        
        assert_true(results is not None)
        assert_equal(results[self.test_mediawiki_user_id]['edits'], 2)
        assert_equal(results[self.test_mediawiki_user_id_evan]['edits'], 3)
    
    def test_reports_zero_edits(self):
        cohort = self.session.query(Cohort).filter_by(name='test').one()
        
        metric = NamespaceEdits()
        results = metric(list(cohort), self.mwSession)
        
        assert_true(results is not None)
        assert_equal(results[self.test_mediawiki_user_id_andrew]['edits'], 0)


class NamespaceEditsFullTest(QueueDatabaseTest):
    
    def test_namespace_edits(self):
        cohort = self.session.query(Cohort).filter_by(name='test').one()
        
        metric = NamespaceEdits()
        report = MetricReport(metric, list(cohort), 'enwiki')
        results = report.task.delay(report).get()
        print 'results: %s' % results
        
        assert_true(results is not None)
        assert_equal(results[self.test_mediawiki_user_id_evan]['edits'], 3)
    
    def test_namespace_edits_namespace_filter(self):
        cohort = self.session.query(Cohort).filter_by(name='test').one()
        
        namespaces = [3]
        metric = NamespaceEdits(namespaces=namespaces)
        report = MetricReport(metric, list(cohort), 'enwiki')
        results = report.task.delay(report).get()
        
        assert_true(results is not None)
        assert_equal(results[self.test_mediawiki_user_id_evan]['edits'], 0)
    
    def test_namespace_edits_namespace_filter_no_namespace(self):
        cohort = self.session.query(Cohort).filter_by(name='test').one()
        
        namespaces = []
        metric = NamespaceEdits(namespaces=namespaces)
        report = MetricReport(metric, list(cohort), 'enwiki')
        results = report.task.delay(report).get()
        
        assert_true(results is not None)
        assert_equal(results[self.test_mediawiki_user_id_evan]['edits'], 0)
    
    def test_namespace_edits_with_multiple_namespaces(self):
        cohort = self.session.query(Cohort).filter_by(name='test').one()
        
        namespaces = [0, 209]
        metric = NamespaceEdits(namespaces=namespaces)
        report = MetricReport(metric, list(cohort), 'enwiki')
        results = report.task.delay(report).get()
        
        assert_true(results is not None)
        assert_equal(results[self.test_mediawiki_user_id]['edits'], 3)
    
    def test_namespace_edits_with_multiple_namespaces_when_passing_string_list(self):
        cohort = self.session.query(Cohort).filter_by(name='test').one()
        
        namespaces = '0, 209'
        metric = NamespaceEdits(namespaces=namespaces)
        report = MetricReport(metric, list(cohort), 'enwiki')
        results = report.task.delay(report).get()
        
        assert_true(results is not None)
        assert_equal(results[self.test_mediawiki_user_id]['edits'], 3)
