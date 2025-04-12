import pytest
from textual.widgets import ListItem

APP_SIZE = (120, 80)


@pytest.mark.parametrize(
    "file_list, amount",
    [
        ([], 0),
        (["test1"], 1),
        (["test1", "test2"], 2),
        (["test1", "test2", "test3"], 3),
    ],
)
async def test_filepanel_file(test_app, test_data_path, file_list, amount):
    for file in file_list:
        if file:
            (test_data_path / file).touch()
            assert (test_data_path / file).exists()

    async with test_app.run_test(size=APP_SIZE) as pilot:
        assert len(list(pilot.app.file_selector.query(ListItem))) == amount
        if file_list:
            assert (
                pilot.app.file_selector.query(ListItem).first().file_name in file_list
            )


@pytest.mark.parametrize(
    "file_list, folder_list, amount",
    [
        ([], [], 0),
        (["test1"], ["."], 1),
        (["test1", "test2"], [".", "folder1"], 4),
        (["test1", "test2", "test3"], ["folder1", "folder2"], 6),
    ],
)
async def test_filepanel_folder(
    test_app, test_data_path, file_list, folder_list, amount
):
    # create files
    for folder in folder_list:
        if not folder:
            folder_path = None
        elif folder == ".":
            folder_path = test_data_path
        else:
            folder_path = test_data_path / folder
            if not folder_path.exists():
                folder_path.mkdir(exist_ok=True)

        for file in file_list:
            if file:
                (folder_path / file).touch()
                assert (folder_path / file).exists()

    # test if files are present in file_selector
    async with test_app.run_test(size=APP_SIZE) as pilot:
        assert len(list(pilot.app.file_selector.query(ListItem))) == amount
        if file_list:
            assert (
                pilot.app.file_selector.query(ListItem).first().file_name in file_list
            )

        if folder_list:
            assert (
                pilot.app.file_selector.query(ListItem).first().dir_name in folder_list
            )
