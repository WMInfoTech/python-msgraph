import os
from msgraph import api, user, files

if __name__ == '__main__':
    import argparse
    authority_host_uri = 'https://login.microsoftonline.com'
    tenant = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    resource_uri = 'https://graph.microsoft.com'
    client_id = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    client_thumbprint = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    parser = argparse.ArgumentParser(description='Microsoft Graph Files Test')
    parser.add_argument('-t', '--tenant', dest='tenant', type=str, help='Microsoft Graph Tenant', default=os.getenv('DATACENTER'))
    parser.add_argument('-c', '--clientid', dest='client_id', type=str, help='Microsoft Graph Client ID', default=os.getenv('CLIENTID'))
    parser.add_argument('--thumbprint', dest='thumbprint', type=str, help='Microsoft Graph Secret', default=os.getenv('CLIENTSECRET'))
    parser.add_argument('--certificate', dest='certificate', type=str, help='Microsoft Graph Certificate', default=os.getenv('CERTIFICATE'))
    parser.add_argument('--user', dest='user', type=str, required=True, help='Microsoft Graph Test User')
    parser.add_argument('--source', dest='src', type=str, required=True, help='Source file to upload')
    parser.add_argument('--filename', dest='filename', type=str, required=True, help='File name to save as')

    args = parser.parse_args()

    if not os.path.exists(args.src):
        raise ValueErr('%r does not exist' % args.src)

    if os.path.exists(args.certificate):
        with open(args.certificate, 'rb') as input_file:
            client_certificate = input_file.read()
    else:
        client_certificate = args.certificate
    api_instance = api.GraphAPI.from_certificate(authority_host_uri, args.tenant, resource_uri, args.client_id, client_certificate, args.thumbprint)

    test_user = user.User.get(api_instance, args.user)
    # fetch a OneDrive of a given user
    drive = files.Drive.get(api_instance, user=test_user)
    # fetch the OneDrive for a given site

    # fetch drives accessible by a given user
    accessible_drives = files.Drive.accessible(api_instance, user=args.user)
    print(accessible_drives)

    # fetch the root folder of the drive
    drive_root_folder = files.DriveItem.root_folder(api_instance, drive=drive)

    # create a new folder in the root folder
    new_folder = files.DriveItem.create_folder(api_instance, "Test", drive_root_folder, drive=drive)

    session = files.Session.create(api, new_folder, file_name=args.filename)
    with open(args.src, 'rb') as input_file:
        session.upload(api, input_file)

    # delete newly created folder
    new_folder.delete(api_instance, drive=drive)
