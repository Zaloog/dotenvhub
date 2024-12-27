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
    # (test_data_path / 'test123').touch()
    # assert (test_data_path/'test123').exists()
    for file in file_list:
        if file:
            (test_data_path / file).touch()
            assert (test_data_path / file).exists()

    async with test_app.run_test(size=APP_SIZE) as pilot:
        assert len(list(pilot.app.file_selector.query(ListItem))) == amount
        if file_list:
            assert (
                pilot.app.file_selector.query(ListItem).first().file_name
                == file_list[0]
            )
