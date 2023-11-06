
DB_NAME = "ip2asn-v4-u32.tsv.gz"



def search_ip(as_df, ip):
    ip_number = int(ipaddress.ip_address(ip))
    row = as_df.query(
        "start_ip <= @ip_number and end_ip >= @ip_number"
    ).iloc[0]

    start_ip = str(ipaddress.ip_address(int(row["start_ip"])))
    end_ip = str(ipaddress.ip_address(int(row["end_ip"])))
    organization = row["organization"]
    asn = row["asn"]
    country = row["country"]

    return {
        "target": ip,
        "asn": int(asn),
        "organization": organization,
        "country": country,
        "start_ip": start_ip,
        "end_ip": end_ip,
    }

def search_by_name(as_df, name, case=True):
    rows = as_df[as_df.organization.str.contains(name, case=case)]

    entries = []
    for _, row in rows.iterrows():
        start_ip = str(ipaddress.ip_address(int(row["start_ip"])))
        end_ip = str(ipaddress.ip_address(int(row["end_ip"])))
        organization = row["organization"]
        asn = row["asn"]
        country = row["country"]

        entries.append({
            "target": name,
            "asn": int(asn),
            "organization": organization,
            "country": country,
            "start_ip": start_ip,
            "end_ip": end_ip,
        })

    return entries

def retrieve_db(db_file=None):
    if db_file:
        return db_file

    db_dir = os.path.join(os.environ["HOME"], DIR_NAME)
    db_file = os.path.join(db_dir, DB_NAME)

    download_again = False
    try:
        m_time = os.path.getmtime(db_file)
        if time.time() - m_time > 60 * 60 * 24 * 1:
            download_again = True
    except FileNotFoundError:
        download_again = True

    if download_again:
        os.makedirs(db_dir, exist_ok=True)
        print("Downloading database...", file=sys.stderr)
        download_db(db_file)

    return db_file

def download_db(path):
    url = "https://iptoasn.com/data/ip2asn-v4-u32.tsv.gz"
    resp = requests.get(url, stream=True)
    total_size = int(resp.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(path, 'wb') as file:
        for data in resp.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
        progress_bar.close()


