# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pprint
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.contrib.pipeline.files import FilesPipeline
from scrapy.exceptions import DropItem
from pprint import pprint as pp


from sqlalchemy.orm import sessionmaker
from models import HKResults, db_connect, create_HKResults_Table

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

# class MyImagesPipeline(ImagesPipeline):
#     pp('**********************===================*******************')
# 	def get_media_requests(self, item, info):
# 		for image_url in item['image_urls']:
# 			yield scrapy.Request(image_url)

class MyFilesPipeline(FilesPipeline):

    # def __init__(self):
    # 	super(ImagesPipeline, self).__init__()
    # 	store_uri = settings.VIDEOS_DIR

    #Name download version
    def file_path(self, request, response=None, info=None):
        item=request.meta['item'] # Like this you can use all from item, not just url.
        #or items['file_urls']
        #file_id = request.url.split('/')[-1]
        return 'full/%s' % (item['file_url'])

    #Name thumbnail version

    def get_media_requests(self, item, info):
        #yield Request(item['images']) # Adding meta.
            yield scrapy.Request(item['files'])


    def media_downloaded(self, response, request, info):
        item = response.meta.get("item")
        video = response.body
        video_basename = item['file_url'][0]
        new_filename = os.path.join(self.VIDEOS_DIR, video_basename)
        f = open(new_filename, 'wb')
        f.write(video)
        f.close()
    # def filekey(self, url):
    #     image_guid = url.split('/')[-1]
    #     return 'full/%s' % (image_guid)

	# def file_path(self, request, response=None, info=None):
	# 	pp("called me yes************************************")
	# 	image_id = item['file_url']
	# 	return 'full/%s' % (image_id)

#     def media_downloaded(self, response, request, info):
#     	pp("ffffffffff")
#         item = response.meta.get("item")
#         video = response.body
#         video_basename = item['video_url'][0]
#         new_filename = os.path.join(self.VIDEOS_DIR, video_basename)
#         f = open(new_filename, 'wb')
#         f.write(video)
#         f.close()
#         return response

#######DATABASE




class HKDBPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_HKResults_Table(engine)
        self.Session = sessionmaker(bind=engine)

    #not working
    def process_item(self, item, spider):
        """Save results to the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        result = HKResults(**item)

        try:
            session.add(result)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
