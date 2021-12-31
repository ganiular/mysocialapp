
def get_post(post_id, cursor):
    cursor.execute(
        "SELECT post.id, post.body, post.image_name, post.created, post.author_id, "
        "user.first_name || ' ' || user.surname as author_name, "
        "COUNT(l_c.likes) as likes, COUNT(l_c.comments) as comments "
        "FROM post "
        "JOIN user ON post.author_id=user.id "
        "LEFT JOIN ( "
        "   SELECT post_id, author_id as likes, NULL AS comments FROM Like WHERE post_id=? "
        "   UNION "
        "   SELECT post_id, NULL, id FROM comment WHERE post_id=? ) "
        "AS l_c ON post.id=l_c.post_id "
        "WHERE post.id = ? LIMIT 1",
        (post_id, post_id, post_id)
    )
    return cursor.fetchone()

def get_posts(cursor):
    "get every posts along with their author name"
    cursor.execute(
        "SELECT post.id, post.body, post.image_name, post.created, post.author_id, "
        "user.first_name || ' ' || user.surname AS author_name, "
        "COUNT(l_c.likes) AS likes, COUNT(l_c.comments) AS comments "
        "FROM post "
        "JOIN user ON post.author_id=user.id "
        "LEFT JOIN ( "
        "   SELECT post_id, author_id AS likes, NULL AS comments FROM Like "
        "   UNION "
        "   SELECT post_id, Null, id FROM comment ) "
        "AS l_c ON post.id=l_c.post_id "
        "GROUP BY post.id "
        "ORDER BY post.id DESC"
    )
    return cursor

def write_post(author_id, body, image_name, cursor):
    cursor.execute(
        "INSERT INTO post(author_id, body, image_name) VALUES(?,?,?)",
        (author_id, body, image_name)
    )
    return cursor.lastrowid

def update_post(post_id, body, image, cursor):
    cursor.execute(
        "UPDATE post SET body=?, image_name=? WHERE id=? LIMIT 1",
        (body, image, post_id)
    )

def delete_post(post_id, cursor):
    cursor.execute("DELETE FROM like WHERE post_id=?", (post_id,))
    cursor.execute("DELETE FROM comment WHERE post_id=?", (post_id,))
    cursor.execute("DELETE FROM post WHERE id=?", (post_id,))

def unlike(post_id, author_id, cursor):
    cursor.execute("DELETE FROM like WHERE post_id=? AND author_id=? LIMIT 1", (post_id, author_id))

def like(post_id, author_id, cursor):
    cursor.execute("INSERT INTO like(post_id, author_id) VALUES(?,?)", (post_id, author_id))

def write_comment(post_id, author_id, body, cursor):
    cursor.execute(
        "INSERT INTO comment(post_id, author_id, body) VALUES(?,?,?)", (post_id, author_id, body)
    )

def get_comments(post_id, cursor):
    cursor.execute(
        "SELECT c.body, c.created, c.author_id, u.first_name || ' ' || u.surname as author_name "
        "FROM comment c "
        "JOIN user u ON c.author_id=u.id "
        "WHERE c.post_id = ? ", (post_id,))
    return cursor
