from simple_ddl_parser import DDLParser

ddl = """CREATE TABLE `employee` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `authority` int(11) DEFAULT '1' COMMENT 'user auth',
  PRIMARY KEY (`user_id`),
  KEY `FK_authority` (`user_id`,`user_name`)
) ENGINE InnoDB;
"""
result = DDLParser(ddl).run(group_by_type=True)

import pprint

pprint.pprint(result)