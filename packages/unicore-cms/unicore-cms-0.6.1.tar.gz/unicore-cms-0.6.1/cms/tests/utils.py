import os
import pygit2
import shutil
import unittest

from unicore_gitmodels import models
from cms import utils


class RepoHelper(object):

    @classmethod
    def create(cls, repo_path, name='Test Kees', email='test@example.org',
               bare=False, commit_message='initialize repository'):
        if not os.path.exists(repo_path):
            repo = pygit2.init_repository(repo_path, bare)
            author = pygit2.Signature(name, email)
            committer = author
            tree = repo.TreeBuilder().write()
            repo.create_commit(
                'refs/heads/master',
                author, committer, commit_message, tree, [])
        return cls(repo_path)

    def __init__(self, repo_path):
        self.repo = pygit2.Repository(repo_path)
        self.ws = utils.get_workspace(self.repo)
        self.ws.register_model(models.GitPageModel)
        self.ws.register_model(models.GitCategoryModel)

    @property
    def path(self):
        return self.repo.path

    @property
    def workdir(self):
        return self.repo.workdir

    def destroy(self):
        try:
            shutil.rmtree(self.workdir)
        except:
            pass
        utils.WORKSPACE_CACHE = {}

    def get_models(self):
        return self.ws.import_models(models)

    def create_categories(
            self, names=[u'Diarrhoea', u'Hygiene'], locale='eng_UK',
            featured_in_navbar=False):
        models = self.get_models()
        categories = []
        for name in names:
            category = models.GitCategoryModel(title=name, language=locale)
            category.featured_in_navbar = featured_in_navbar
            category.slug = category.slugify(name)
            category.save(True, message=u'added %s Category' % (name,))
            categories.append(
                models.GitCategoryModel().get(category.uuid))

        return categories

    def create_pages(self, count=2, timestamp_cb=None, locale='eng_UK'):
        timestamp_cb = timestamp_cb or (lambda i: None)
        models = self.get_models()
        pages = []
        for i in range(count):
            page = models.GitPageModel(
                title=u'Test Page %s' % (i,),
                content=u'this is sample content for pg %s' % (i,),
                modified_at=timestamp_cb(i),
                language=locale)
            page.save(True, message=u'added page %s' % (i,))
            pages.append(models.GitPageModel().get(page.uuid))

        return pages


class BaseTestCase(unittest.TestCase):
    pass
