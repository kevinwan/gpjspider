from gpjspider.utils.phone_parser import ConvertPhonePic2Num
from gpjspider.utils import get_mysql_connect
import logging

log_filename = '/tmp/gpjspider/validate_phone_pattern.log'
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
Session = get_mysql_connect()
session = Session()
sql='''
select
    phone
from open_product_source
where 1=1
--    and created_on>curdate()
    and domain='taoche.com'
    and phone like 'http%'
order by id desc
limit 100
'''.strip()
urls = [row[0] for row in session.execute(sql)]
valid_ratio = ConvertPhonePic2Num.valid_taoche(urls)
print valid_ratio
session.execute('insert into open_monitor_indicator(name,the_time,val)values("TaochePhonePattern", now(), %d)' % valid_ratio)
session.commit()
print 'done'