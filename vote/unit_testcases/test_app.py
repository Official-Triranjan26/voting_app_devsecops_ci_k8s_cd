import json
import unittest
from unittest.mock import patch

import app


class VoteRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_get_displays_voting_page_and_sets_voter_cookie(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cats", response.data)
        self.assertIn(b"Dogs", response.data)
        self.assertTrue(response.headers.get("Set-Cookie", "").startswith("voter_id="))

    @patch("app.get_redis")
    def test_post_enqueues_vote_with_voter_id(self, get_redis):
        redis = get_redis.return_value

        response = self.client.post("/", data={"vote": "a"})

        self.assertEqual(response.status_code, 200)
        redis.rpush.assert_called_once()
        queue_name, message = redis.rpush.call_args.args
        self.assertEqual(queue_name, "votes")
        payload = json.loads(message)
        self.assertEqual(payload["vote"], "a")
        self.assertTrue(payload["voter_id"])

    @patch("app.get_redis")
    def test_repeat_post_uses_existing_voter_id(self, get_redis):
        redis = get_redis.return_value

        self.client.get("/")
        voter_id = self.client.get_cookie("voter_id").value
        self.client.post("/", data={"vote": "b"})

        payload = json.loads(redis.rpush.call_args.args[1])
        self.assertEqual(payload["voter_id"], voter_id)


if __name__ == "__main__":
    unittest.main()
