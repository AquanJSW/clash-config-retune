from .public import *
from modules import utils


class ProxyIP:
    def __init__(self, proxy: dict, ip: Iterable) -> None:
        self.proxy = proxy
        self.ip = tuple(ip)
        self.__hash = hash(self.ip)

    def __hash__(self) -> int:
        return self.__hash

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o)


class Retune:
    def __init__(self, config, template, output) -> None:
        """
        Argument
        ---
        See argparser in 'scripts/retune.py' for details.
        """
        self.config = Retune.__get_config(config)
        self.template = Retune.__get_config(template, 'template')
        self.pathSave = output
        self.sProxyIP = self.__get_sProxyIP()

    def __get_sProxyIP(self):
        sProxy = self.config['proxies']

        sProxyIP = set(self.__filter_nonGlobal_(Retune.__is_global, sProxy))
        '''Global and non-duplicated.'''

        return sProxyIP

    def dump_withOriginName(self):
        self.__dump([x.proxy for x in self.sProxyIP])

    def __dump(self, proxies: Iterable):
        dst = deepcopy(self.template)

        # Add proxies
        dst['proxies'] = proxies

        # Add proxy-groups
        lNames = [proxy['name'] for proxy in proxies]
        try:
            dst['proxy-groups']
            for g in dst['proxy-groups']:
                g['proxies'] = lNames
        except KeyError:
            dst['proxy-groups'] = []

        dst['proxy-groups'].append(
            {'name': 'PROXY', 'type': 'select', 'proxies': lNames}
        )
        with open(self.pathSave, 'w', encoding='utf-8') as fp:
            yaml.safe_dump(dst, fp, allow_unicode=True)
        if verbose:
            print("Retuned config file has been saved to {}".format(self.pathSave))

    def __filter_nonGlobal_(self, fn, iterable):
        retVal = []
        for it in tqdm(iterable, disable=not verbose):
            retVal.append(fn(it))
        return list(filter(lambda x: x, retVal))
            

    def __filter_nonGlobal(self, fn, iterable):
        retVal = process_map(
            fn, iterable, desc='Filtering non-global proxies.', unit='proxy'
        )
        return list(filter(lambda x: x, retVal))

    @staticmethod
    def __is_global(proxy: dict):
        """If the server valid?

        Return
        ---
        Instance of `ProxyIP` if true, else `False`.
        """
        server = proxy['server']
        try:
            addr = ipaddress.ip_address(server)
            if addr.is_global:
                return ProxyIP(proxy, [server])
        except ValueError:
            lIP = Nslookup(['8.8.8.8']).dns_lookup_all(server).answer
            for ip in lIP:
                addr = ipaddress.ip_address(ip)
                if not addr.is_global:
                    return False
            return ProxyIP(proxy, sorted(lIP))
        return False

    @staticmethod
    def __get_config(conf, name='config'):
        """From file or URL."""

        if utils.is_file(conf):  # from file
            with open(conf, mode='r', encoding='utf-8') as f:
                try:
                    ret = yaml.safe_load(f)
                except BaseException:
                    print('error loading {} from file'.format(name))
                    raise
        else:  # from url
            try:
                headers = {'charset': 'utf-8'}
                r = requests.get(url=conf, headers=headers)
                ret = yaml.safe_load(r.text)
            except BaseException:
                print('error loading {} from url'.format(name))
                raise

        return ret
