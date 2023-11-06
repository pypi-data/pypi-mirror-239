
import ipaddress

class CloudRangeDb:

    def __init__(self) -> None:
        db_file = self.retrieve_db()
        self.db = self.prepare_db(db_file)

    @classmethod
    def retrieve_db(cls):
        raise NotImplementedError()

    @classmethod
    def prepare_db(cls, db_file):
        raise NotImplementedError()

    @classmethod
    def name(cls):
        raise NotImplementedError()

    def search_ip(self, ip):
        return search_ip(self.name(), self.db, ip)


def search_ip(cloud_name, db, ip):
    ip_addr = ipaddress.ip_address(ip)
    ip_number = int(ip_addr)
    ip_version = ip_addr.version
    result = db.query(
        "version == @ip_version"
        " and start_ip <= @ip_number"
        " and end_ip >= @ip_number"
    )
    if result.empty:
        raise KeyError(ip)

    row = result.iloc[0]

    services =  [s for s in result["service"] if s]
    region = row["region"]

    return {
        "cloud": cloud_name,
        "services": services,
        "region": region,
        "network": row["network"],
    }

