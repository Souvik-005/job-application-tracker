import pytest

from src.tracker.database import (
    init_db,
    add_application,
    get_all_applications,
    get_application,
    update_status,
    delete_application,
    get_due_followups,
)
from src.tracker.models import Application, Status


@pytest.fixture
def db(tmp_path):
    path = str(tmp_path / "test.db")
    init_db(path)
    return path


def test_add_and_get_application(db):
    new_id = add_application(Application("Google", "Python Developer"), db)
    app = get_application(new_id, db)
    assert app.company == "Google"
    assert app.title == "Python Developer"
    assert app.status == Status.APPLIED


def test_get_missing_application_returns_none(db):
    assert get_application(999, db) is None

def test_get_all_applications(db):
    add_application(Application("Google", "Python Developer"), db)
    add_application(Application("Amazon", "Backend Engineer"), db)
    assert len(get_all_applications(db_path=db)) == 2


def test_update_status(db):
    new_id = add_application(Application("Google", "Python Developer"), db)
    update_status(new_id, Status.INTERVIEW, db)
    app = get_application(new_id, db)
    assert app.status == Status.INTERVIEW


def test_delete_application(db):
    new_id = add_application(Application("Google", "Python Developer"), db)
    assert delete_application(new_id, db) is True
    assert get_application(new_id, db) is None

def test_filter_by_status(db):
    add_application(Application("Google", "Dev"), db)
    id2 = add_application(Application("Amazon", "Dev"), db)
    update_status(id2, Status.INTERVIEW, db)
    result = get_all_applications(status=Status.INTERVIEW, db_path=db)
    assert len(result) == 1
    assert result[0].company == "Amazon"


def test_due_followups(db):
    add_application(Application("Google", "Dev", follow_up_date="2026-11-10"), db)
    add_application(Application("Amazon", "Dev", follow_up_date="2026-12-25"), db)
    add_application(Application("Meta", "Dev"), db)
    result = get_due_followups("2026-11-19", db)
    assert [a.company for a in result] == ["Google"]