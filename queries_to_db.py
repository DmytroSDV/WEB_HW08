from ctypes import Union

from customs.custom_logger import my_logger
from customs.custom_vizualization import vizualization

from conn_modd.models import Author, Quote
import conn_modd.connect

import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def available_commands():
    command_list = ['tag', 'tags', 'name', 'exit']
    command_explain = ["search data in the db by the tag. Use it on format 'tag:life' and then press enter",
                       "search data in the db by the tags. Use it on format 'tags:life,live' and then press enter",
                       "search data in the db by the name. Use it on format 'name:Steve Martin' and then press enter",
                       'application shutdown']
    return ''.join('|{:<5} - {:<20}|\n'.format(command_list[item], command_explain[item]) for item in range(len(command_list)))

@cache
@vizualization
def get_by_tag(input: str):

    command, value = input.split(':', 1)
    tag_list = value.split(",")

    my_logger.log(f"{command.upper()} command execution!")

    result_list = []
    for item in tag_list:
        result_list.append(Quote.objects(tags__iregex=item.strip()))  

    result = [{q.author.fullname:q.quote for q in elem} for elem in result_list]

    return result

@cache
@vizualization
def get_by_name(input: str):

    command, value = input.split(':', 1)
    my_logger.log(f"{command.upper()} command execution!")

    authors = Author.objects(fullname__iregex=value.strip())
    result = {}
    result_list = []
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    result_list.append(result)

    return result_list

def main():

    while 1:
        my_logger.log("To see available list of commands enter 'show'.")
        input_from_user = input(":>>> ")

        if input_from_user.lower() == 'show':
            my_logger.log(available_commands())

        elif (input_from_user.lower().find('tag:') != -1 or 
                input_from_user.lower().find('tags:') != -1):
            get_by_tag(input_from_user)

        elif input_from_user.lower().find('name:') != -1:
            get_by_name(input_from_user)

        elif input_from_user.lower().find('exit') != -1:
            my_logger.log('Application shutdown! Bye bye!')
            break

        else:
            my_logger.log(f"Sorry your enter wrong command '{input_from_user}'\nPlease choose available command from the below list!\n")
            my_logger.log(available_commands())

if __name__ == '__main__':
    main()