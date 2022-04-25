from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from monster.models import create_table, db_connect, MonsterJob
import monster.settings


class SaveJobPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()
        job = MonsterJob()
        job.Location = item["Location"]
        job.JobId = item["JobId"]
        job.Title = item["Title"]
        job.Company = item["Company"]
        job.Description = item["Description"]
        job.Country = item["Country"]

        try:
            session.add(job)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


class CheckForDuplicatesPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        item_exists = session.query(MonsterJob).filter_by(JobId=item["JobId"]).first()
        if item_exists is not None:
            session.close()
            raise DropItem("Duplicate item found and droped: %s" % item["JobId"])

        else:
            session.close()
            return item
