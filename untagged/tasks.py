# -*- encoding: utf-8

import enum

from . import celery, sess


class States(enum.Enum):
    failure = 'FAILURE'
    pending = 'PENDING'
    progress = 'PROGRESS'
    success = 'SUCCESS'


@celery.task(bind=True)
def find_untagged_posts_task(self, hostname):
    """Background task that runs a long function with progress reports."""
    self.update_state(state=States.pending)

    # Make an initial request to the Tumblr API.  This checks that
    # our API key is correct and that the hostname exists.
    try:
        initial_resp = sess.get_posts(hostname=hostname)
    except RuntimeError as err:
        self.update_state(
            state=States.failure,
            meta={
                'message': err.args[0],
            }
        )
        return

    # If the initial request works, we can report the total posts
    # and the initial batch of untagged posts to the user.
    post_count = resp.post_count()
    posts = resp.untagged_posts()
    total_posts = resp.total_posts()
    self.update_state(
        state=States.progress,
        meta={
            'posts': posts,
            'post_count': post_count,
            'total_posts': total_posts,
        }
    )

    # Now fetch the remaining posts.  The Tumblr API doles out posts in
    # batches of 20.
    # TODO: This logic should be contained in tumblr.py, but I haven't
    # tidied it up yet.
    for offset in range(20, (post_count // 20) * 20, 20):
        try:
            resp = sess.get_posts(hostname=hostname, offset=offset)
        except RuntimeError as err:
            self.update_state(
                state=States.failure,
                meta={
                    'message': err.args[0],
                }
            )
            return

        post_count += resp.post_count()
        posts.extend(resp.untagged_posts())
        self.update_state(
            state=States.progress,
            meta={
                'posts': posts,
                'post_count': post_count,
                'total_posts': total_posts,
            }
        )

    return {
        'posts': posts,
        'post_count': post_count,
        'total_posts': total_posts,
    }
