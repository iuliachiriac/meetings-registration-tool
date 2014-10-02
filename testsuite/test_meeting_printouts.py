from flask import url_for
from pyquery import PyQuery

from .factories import ParticipantFactory, MeetingCategoryFactory


def test_shortlist_printout(app):
    cat = MeetingCategoryFactory(sort=1)
    cat_staff = MeetingCategoryFactory(meeting=cat.meeting,
                                       title__english='Staff',
                                       sort=2)
    cat_obs = MeetingCategoryFactory(meeting=cat.meeting,
                                     title__english='Observer',
                                     sort=3)
    categs = [cat, cat_staff, cat_obs]
    ParticipantFactory.create_batch(25, meeting=cat.meeting, category=cat)
    ParticipantFactory.create_batch(25, meeting=cat.meeting,
                                    category=cat_staff)
    ParticipantFactory.create_batch(25, meeting=cat.meeting,
                                    category=cat_obs)

    client = app.test_client()
    with app.test_request_context():
        #TEST FIRST PAGE
        resp = client.get(url_for('meetings.printouts_short_list',
                                  meeting_id=cat.meeting.id))
        assert resp.status_code == 200
        html = PyQuery(resp.data)
        assert len(html('.printout-table tbody tr')) == 52
        groups = html('th.group')
        for group in groups:
            categs.pop(0).title.english == group.text.strip()

        participant_names = html('td#participant-name')
        participant_ids = set([x.attrib['data-id'] for x in participant_names])
        assert len(participant_ids) == 50

        #TEST SECOND PAGE
        resp = client.get(url_for('meetings.printouts_short_list',
                                  meeting_id=cat.meeting.id,
                                  page=2))
        assert resp.status_code == 200
        html = PyQuery(resp.data)
        assert len(html('.printout-table tbody tr')) == 26
        assert categs.pop().title.english == html('th.group').text().strip()
        participant_names = html('td#participant-name')
        for participant in participant_names:
            participant_ids.add(participant.attrib['data-id'])
        assert len(participant_ids) == 75

        #TEST 404 PAGE
        resp = client.get(url_for('meetings.printouts_short_list',
                                  meeting_id=cat.meeting.id,
                                  page=3))
        assert resp.status_code == 404