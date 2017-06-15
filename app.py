"""
    Usage:
        mail <query>
        phone <query>
        twitter <query>
"""

from docopt import docopt,DocoptExit
from functions import FullContact
import cmd, os, sys
from termcolor import colored,cprint
from prettytable import *



def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match
            # We print a message to the user and the usage block
            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def intro():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(__doc__)

def whois(criteria,args):
    if criteria == 'email':
        data = FullContact.whois(email = args["<query>"])
    elif criteria == 'phone':
        data = FullContact.whois(phone = args["<query>"])
    elif criteria == 'twitter':
        data = FullContact.whois(twitter = args["<query>"])
    if isinstance(data, str):
        print(colored(data,'red', attrs = ['bold']))
    else:
        if data["status"] is not 200 : 
            print(colored('\t\t\t\t'+data["message"], 'red', attrs=['bold']))
            print(colored('\t\t\t\t\t\t\tSTATUS: '+str(data["status"]), 'red', attrs=['bold']))
        else:
            print(colored('\t\t\t\tID: '+data["requestId"], 'green', attrs=['bold']))
            print(colored('\t\t\t\t\t\t\tSTATUS: '+str(data["status"]), 'green', attrs=['bold']))
            datasheet = PrettyTable(['#','Info'])
            try:
                datasheet.add_row(['Full Name',data['contactInfo']['fullName']])
            except KeyError:
                pass
            try:
                datasheet.add_row(['Given Name',data['contactInfo']['givenName']])
            except KeyError:
                pass
            try:
                datasheet.add_row(['Location',data['demographics']['locationDeduced']['normalizedLocation']])
            except KeyError:
                pass
            try:
                datasheet.add_row(['Gender',data['demographics']['gender']])
            except KeyError:
                pass 
            social = PrettyTable(['Social Network','url','usermname','id'])
            for profile in data['socialProfiles']:
                social.add_row([profile['typeName'], profile['url'],profile['username'],profile['id']])
            print(datasheet)
            print(social)


class FContact(cmd.Cmd):
    text = colored('FullContact$$$', 'green', attrs=['blink'])
    prompt = text

    @docopt_cmd
    def do_mail(self,args):
        """Usage: mail <query>"""
        whois('email', args =  args)

    @docopt_cmd
    def do_phone(self,args):
        """Usage: phone <query>"""
        whois('phone',args)

    @docopt_cmd
    def do_twitter(self,args):
        """Usage: twitter <query>"""
        whois('twitter',args)

    @docopt_cmd
    def do_quit(self, arg):
        """Usage: quit"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print ('Full Contact has quit')
        exit()


if __name__ == "__main__":
    try:
        intro()
        FContact().cmdloop()
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Full Contact has quit')
