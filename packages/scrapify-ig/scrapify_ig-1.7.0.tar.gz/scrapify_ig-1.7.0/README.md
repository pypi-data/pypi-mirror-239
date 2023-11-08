<h1 style="text-align: center">Python Instagram Scraper API SDK</h1>

---

Library - wrapper over instagrapi scraper API. 

Used by API: https://rapidapi.com/fama-official-instagram-scraper/api/instagram-scraper-api2

This library provides basic data retrieval features with instagram: Users, Posts, Comments, etc. Read more below.

---

## Warning:
It’s just a wrapper on the API.  If the API stops working, the library stops working.

---

## Quick Access:
+ [Get started](https://gitlab.com/oleksii.stulen.public/scrapify-ig/#get-started)
+ [Available features](https://gitlab.com/oleksii.stulen.public/scrapify-ig/#available-features)
+ [Coming soon](https://gitlab.com/oleksii.stulen.public/scrapify-ig/#coming-soon)
+ [Installation](https://gitlab.com/oleksii.stulen.public/scrapify-ig/#installation)
+ [Usage](https://gitlab.com/oleksii.stulen.public/scrapify-ig/#usage)
+ [Examples](https://gitlab.com/oleksii.stulen.public/scrapify-ig/-/tree/master/examples/index.md)
+ [Types](https://gitlab.com/oleksii.stulen.public/scrapify-ig/#types)
+ [Errors and Issues](https://gitlab.com/oleksii.stulen.public/scrapify-ig/#errors-and-issues)
---

<h2 id="get-started" style="text-align: center">Get Started</h2>

## Available features:
+ Get User info
+ Get User medias with pagination
+ Get User Followers with pagination
+ Get Media Post info
+ Get Media Post Comments with pagination
+ Get Media Posts by Tagged user
+ Get Media Posts by Hashtag
+ Get Similar Users
+ Search Users, Hashtags and Places
+ Get Media Post Likes with pagination

---

## Coming soon:
+ Get User Following with pagination
+ Get User Stories
+ Get Story Info
+ Get User Highlights

---

## Installation:

## Pre-requirements:
+ **Python >= 3.9v**


## With pip (https://pypi.org/project/scrapify-ig/):

```shell
pip install scrapify-ig
```

---

## Usage:

+ Before using the library, you need to get the RapidAPI API:
https://rapidapi.com/fama-official-instagram-scraper/api/instagram-scraper-api2

Use the client object to use all possible library functions. Create client object:
```python
from scrapify_ig import Client

TOKEN = "<RapidAPI Token>"

client = Client(token=TOKEN)
```

Now you are ready to use the library. 

**Get user information:**

See [examples/user_info.md](examples/user_info.md) for more details

```python
user_info = client.get_user_info(username_or_id_or_url="nike", include_about=False, url_embed_safe=False)

# Returns: types.User instance
```

**Get user media posts:**

See [examples/user_medias.md](examples/user_medias.md) for more details

```python
from scrapify_ig import types, exceptions

user_medias_chunk: types.MediaPostsChunk = client.get_user_medias_chunk(
    username_or_id_or_url="nike",
    url_embed_safe=False
)

# Returns: types.MediaPostsChunk.
# Posts are available in the data field: user_medias.data.

# To get the next chank, call again get_user_medias_chunk again and specify the pagination_token argument. 
# pagination_token is the object field types.MediaPostsChunk. 
# Example:

next_user_medias_chunk: types.MediaPostsChunk = client.get_user_medias_chunk(
    username_or_id_or_url="nike", 
    pagination_token=user_medias_chunk.pagination_token
)

# OR:
# You can use the interface .next_chunk:

next_users_medias_chunk: types.MediaPostsChunk = user_medias_chunk.next_chunk()

# Warning: 
# .next_chunk throws exceptions.NoNextPageError an error if there is no next page. 
# It is recommended to use first check that there is the following page. 
# Example:

if user_medias_chunk.has_next_chunk():
    next_users_medias_chunk: types.MediaPostsChunk = user_medias_chunk.next_chunk()

# OR:

try:
    next_users_medias_chunk: types.MediaPostsChunk = user_medias_chunk.next_chunk()
except exceptions.NoNextPageError:
    # do something
    pass

```

**Get user followers:**
```python
from scrapify_ig import types

username = "nike"
user_followers_chunk: types.FollowersChunk = client.get_followers_chunk(username)

next_user_followers_chunk: types.FollowersChunk = client.get_followers_chunk(
    username, 
    pagination_token=user_followers_chunk.pagination_token
)

# Also works .next_chunk interface:

next_user_followers_chunk: types.FollowersChunk = user_followers_chunk.next_chunk()
```

---

**Get Media Post info:**

See [examples/media_info.md](examples/media_info.md) for more details

```python
from scrapify_ig import types

media_identifier = "Cx8yen-uS-d"  # media code, id or url

media_info: types.MediaPost = client.get_media_info(
    code_or_id_or_url=media_identifier,
    url_embed_safe=False
)
```

---

**Get Media Post Comments:**
```python
from scrapify_ig import types, exceptions

media_identifier = "Cx8yen-uS-d"  # media code, id or url
media_comments_chunk: types.CommentsChunk = client.get_media_comments_chunk(
    code_or_id_or_url=media_identifier
)

# Also works .next_chunk interface:
if media_comments_chunk.has_next_chunk():
    next_media_comments_chunk: types.CommentsChunk = media_comments_chunk.next_chunk()


# Note:
# Comments have answers to comments. There are no answers to comments. 
# You need to call client.get_comment_thread_chunk to get answers to a specific comment.
# Example:

some_comment_with_child: types.CommentsChunkItem = media_comments_chunk.data.items[6]
child_comments_chunk: types.CommentsThreadChunk = some_comment_with_child.get_comment_thread_chunk(client)

# OR:
child_comments_chunk: types.CommentsThreadChunk = client.get_comment_thread_chunk(
    comment_id=some_comment_with_child.id
)

# Warning:
# If there is no child comment, the HTTPNotFoundError exception will be discarded
# use the .has_thread_comments method to prevent the error:

if some_comment_with_child.has_thread_comments():
    child_comments_chunk: types.CommentsThreadChunk = client.get_comment_thread_chunk(
        comment_id=some_comment_with_child.id
    )

# OR:
try:
    child_comments_chunk: types.CommentsThreadChunk = client.get_comment_thread_chunk(
        comment_id=some_comment_with_child.id
    )
except exceptions.HTTPNotFoundError:
    # do something
    pass
```

**Get Media Posts by Tagged user:**
```python
from scrapify_ig import types

user_identifier = "nike"

tagged_posts_chunk: types.TaggedMediaPostsChunk = client.get_tagged_medias_chunk(
    username_or_id_or_url=user_identifier
)

# Also works .next_chunk interface:
if tagged_posts_chunk.has_next_chunk():
    next_tagged_posts_chunk: types.TaggedMediaPostsChunk = tagged_posts_chunk.next_chunk()

# OR:
next_tagged_posts_chunk: types.TaggedMediaPostsChunk = client.get_tagged_medias_chunk(
    username_or_id_or_url=user_identifier,
    pagination_token=tagged_posts_chunk.pagination_token
)
```

**Get Media Posts by Hashtag:**
```python
from scrapify_ig import types

hashtag = "nike"

hashtag_medias_chunk: types.MediaPostsHashtagChunk = client.get_medias_by_hashtag_chunk(
    hashtag=hashtag
)

# Also works .next_chunk interface:
if hashtag_medias_chunk.has_next_chunk():
    next_hashtag_medias_chunk: types.MediaPostsHashtagChunk = hashtag_medias_chunk.next_chunk()

# OR:
next_hashtag_medias_chunk: types.MediaPostsHashtagChunk = client.get_medias_by_hashtag_chunk(
    hashtag=hashtag,
    pagination_token=hashtag_medias_chunk.pagination_token
)
```

**Get Similar Users:**
```python
from scrapify_ig import types

user_identifier = "nike"

similar_accounts: types.SimilarAccounts = client.get_similar_accounts(
    username_or_id_or_url=user_identifier
)

# Note:
# pagination not allowed
```

**Search Users, Hashtags and Places:**
```python
from scrapify_ig import types

search_query = "London"

search_result: types.SearchResult = client.search(search_query=search_query)

# Note:
# pagination not allowed
```

**Get Media Post Likes with pagination:**
```python
from scrapify_ig import types

media_identifier = "Cx8yen-uS-d"  # media code, id or url

media_likes_chunk: types.LikesMediaPostsChunk = client.get_media_likes_chunk(
    code_or_id_or_url=media_identifier
)


# Also works .next_chunk interface:
if media_likes_chunk.has_next_chunk():
    media_likes_chunk: types.LikesMediaPostsChunk = media_likes_chunk.next_chunk()
```

## Types:
+ user scrapify_ig.types for better typing. Also in this module you can see all available fields for each object

---

## Errors and Issues:
If you notice an error or problem, please write about it here https://gitlab.com/oleksii.stulen.public/scrapify-ig/issues. Describe the problem as precisely as possible. What did you do, what did you want to get, how did you do it and so on. Thank you!

---

Author: Oleksii Stulen

Email: oleksii.stulen.workspace@gmail.com
