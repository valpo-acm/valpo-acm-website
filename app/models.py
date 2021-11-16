import os
import mariadb
from dotenv import load_dotenv

TABLES = {
    'eboard':("eboard_id int NOT NULL AUTO_INCREMENT PRIMARY KEY", "eboard_position VARCHAR(32) NOT NULL", "eboard_description TEXT"),
    'member':("member_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY", "first_name VARCHAR(32) NOT NULL", "last_name VARCHAR(32) NOT NULL", "middle_name VARCHAR(32)", "valpo_email VARCHAR(64)", "secondary_email VARCHAR(64)", "major VARCHAR(32)", "grad_year INT", "grad_month VARCHAR(9)", "bio MEDIUMTEXT", "fav_language VARCHAR(64)", "curr_eboard_pos_id INT", "current_job TINYTEXT", "favorite_memory LONGTEXT", "is_alumnus BOOLEAN", "FOREIGN KEY (curr_eboard_pos_id) REFERENCES eboard(eboard_id)"),
    'project':("project_id int NOT NULL AUTO_INCREMENT PRIMARY KEY", "project_name VARCHAR(128) NOT NULL", "github_link VARCHAR(128)", "gource_url VARCHAR(128)", "readme LONGTEXT", "demo_video_url VARCHAR(128)", "start_date DATETIME", "end_date DATETIME"),
    'member_eboard_positions':("member_id int NOT NULL", "eboard_id int NOT NULL", "start DATETIME", "end DATETIME", "CONSTRAINT PK_member_eboard_positions PRIMARY KEY (member_id, eboard_id)", "FOREIGN KEY (member_id) REFERENCES member(member_id)", "FOREIGN KEY (eboard_id) REFERENCES eboard(eboard_id)"),
    'member_project_contributions':("member_id int NOT NULL", "project_id int NOT NULL", "CONSTRAINT PK_member_eboard_positions PRIMARY KEY (member_id, project_id)", "FOREIGN KEY (member_id) REFERENCES member(member_id)", "FOREIGN KEY (project_id) REFERENCES project(project_id)")
}
load_dotenv()
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': os.environ['DB_PASSWORD']
}
conn = mariadb.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("SHOW DATABASES;")
if ("acm_website",) not in cur.fetchall():
    create_db()
else:
    cur.execute("USE acm_website;")

class Member:

    # all_eboard_positions should be a list of dicts of the form {position:"President", start:"2021-08-01", end:"2022-05-31"}
    def __init__(self, first_name, last_name, middle_name=None, valpo_email=None, secondary_email=None, major=None, grad_year=None, grad_month=None, bio=None, fav_language=None, current_job=None, favorite_memory=None, is_alumnus=None, curr_eboard_pos=None, all_eboard_positions=None):
        self.unique_id = None
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.valpo_email = valpo_email
        self.secondary_email = secondary_email
        self.major = major
        self.grad_year = grad_year
        self.grad_month = grad_month
        self.bio = bio
        self.fav_language = fav_language
        self.current_job = current_job
        self.favorite_memory = favorite_memory
        self.is_alumnus = is_alumnus
        self.curr_eboard_pos = curr_eboard_pos
        self.all_eboard_positions = all_eboard_positions

    def save_new_to_db(self):
        attributes = dir(self)
        attributes.remove("unique_id")
        attributes.remove("curr_eboard_pos")
        attributes.remove("all_eboard_positions")
        values = (f"{getattr(self, att)}" for att in attributes)
        former_eboard_pos = []
        if self.curr_eboard_pos!=None or self.all_eboard_positions!=None:
            cur.execute("SELECT eboard_id, eboard_position FROM eboard;")
            eboard_positions = cur.fetchall()
            if self.curr_eboard_pos!=None:
                for p in eboard_positions:
                    curr_eboard_id = 0
                    if self.curr_eboard_pos.lower()==p[1].lower():
                        curr_eboard_id = p[0]
                        break
                if curr_eboard_id:
                    attributes.append("curr_eboard_pos_id")
                    values.append(curr_eboard_id)
            if self.all_eboard_positions!=None:
                former_eboard_pos = self.all_eboard_positions.copy()
                for i, position in enumerate(former_eboard_pos):
                    for p in eboard_positions:
                        if p[1].lower()==position['position'].lower():
                            former_eboard_pos[i]['id']=p[0]
            elif curr_eboard_id:
                former_eboard_pos.append({
                    "position":self.curr_eboard_pos,
                    "start":None,
                    "end":None,
                    "id":values[-1]
                })
        attributes = str(attributes).replace("'","").replace('"','')
        values = str(values).replace("'","").replace('"','')
        cur.execute(f"INSERT INTO member{attributes} VALUES {values};".replace("None","NULL"))
        conn.commit()
        cur.execute(f"SELECT member_id FROM member ORDER BY member_id DESC LIMIT 1;")
        id = cur.fetchall()[0][0]
        for position in former_eboard_pos:
            cur.execute(f"INSERT INTO member_eboard_positions(member_id,eboard_id,start,end) VALUES ({id},{position['id']},{position['start']},{position['end']});".replace("None","NULL"))
        conn.commit()

class Eboard:

    def __init__(self, eboard_position, eboard_description=None):
        self.unique_id = None
        self.eboard_position = eboard_position
        self.eboard_description = eboard_description

    def __setitem__(self,key,value):
        if key not in dir(self):
            return False
        setattr(self,key,value)
        cur.execute(f"UPDATE eboard SET {key} = {value} WHERE eboard_id={self.unique_id};")
        conn.commit()

    def save_new_to_db(self):
        attributes = dir(self)
        values = (f"{getattr(self, att)}" for att in attributes)
        attributes = str(attributes).replace("'","").replace('"','')
        values = str(values).replace("'","").replace('"','')
        cur.execute(f"INSERT INTO member{attributes} VALUES {values};".replace("None","NULL"))
        conn.commit()

    def load_all():
        cur.execute("SELECT * FROM eboard;")
        eboard = cur.fetchall()
        positions = []
        for position in eboard:
            next_pos = Eboard(position[1],position[2])
            next_pos.unique_id = position[0]
            positions.append(next_pos)
        return positions


class Project:

    def __init__(self, project_name, github_link=None, gource_url=None, readme=None, demo_video_url=None, start_date=None, end_date=None, members=None):
        self.project_name = project_name
        self.github_link = github_link
        self.gource_url = gource_url
        self.readme = readme
        self.demo_video_url = demo_video_url
        self.start_date = start_date
        self.end_date = end_date
        self.members = members

def create_db():
    cur.execute("CREATE DATABASE acm_website;")
    cur.execute("USE acm_website;")
    apos = "'"
    for table, columns in TABLES.items():
        print(f"CREATE TABLE {table} {str(columns).replace(apos,'')};")
        cur.execute(f"CREATE TABLE {table} {str(columns).replace(apos,'')};")
