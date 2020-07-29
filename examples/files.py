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

    args = parser.parse_args()

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
    # drive = files.Drive.get(api_instance, site='a258178f-da15-42dd-a85b-90dbe49ebd9e')

    # fetch drives accessible by a given user
    accessible_drives = files.Drive.accessible(api_instance, user=args.user)
    print(accessible_drives)

    # fetch the root folder of the drive
    drive_root_folder = files.DriveItem.root_folder(api_instance, drive=drive)

    # create a new folder in the root folder
    new_folder = files.DriveItem.create_folder(api_instance, "Test", drive_root_folder, drive=drive)
    # create a file in the new folder
    new_file = files.DriveItem.upload(api_instance, 'Hello, World!', drive=drive, parent=new_folder, file_name='This is a test.txt')

    # overwrite the file in the new folder
    overwriting_file = files.DriveItem.upload(api_instance, 'Hello, John!', drive=drive, parent_id=new_folder, item=new_file, replace=True)

    # update the file name of the file
    overwriting_file.name = 'My new file name.txt'
    overwriting_file.update(api_instance, drive=drive)
    # or alternatively
    overwriting_file.move(api_instance, 'My new file name.txt', folder=drive_root_folder, drive=drive)

    # search for .txt files on the drive
    search_results = files.DriveItem.search(api_instance, 'txt', drive=drive)
    # delete the created file
    overwriting_file.delete(api_instance, drive=drive)

    # fetch children of the root directory of a drive
    root_children = files.DriveItem.get_children(api_instance, drive=drive)
    # fetch children of parent folder
    folder_children = files.DriveItem.get_children(api_instance, drive=drive, parent=new_folder)
    # fetch files by relative path from root of drive
    path_children = files.DriveItem.get_children(api_instance, drive=drive, path='Microsoft Teams Chat Files')
    print(path_children)

    # delete newly created folder
    new_folder.delete(api_instance, drive=drive)
