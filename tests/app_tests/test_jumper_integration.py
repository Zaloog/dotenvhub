from textual.widgets import Button
from textual_jumper import Jumper

APP_SIZE = (120, 80)


async def test_jumper_widget_present(test_app):
    """Test that Jumper widget is present in the app"""
    async with test_app.run_test(size=APP_SIZE) as pilot:
        jumper = pilot.app.query_one(Jumper)
        assert jumper is not None
        assert isinstance(jumper, Jumper)


async def test_jumper_show_action(test_app):
    """Test that action_show_jumper method exists and works"""
    async with test_app.run_test(size=APP_SIZE) as pilot:
        # Test that the action method exists
        assert hasattr(pilot.app, "action_show_jumper")

        # Test that jumper can be queried
        jumper = pilot.app.query_one(Jumper)
        assert jumper is not None

        # Test that action runs without error
        pilot.app.action_show_jumper()
        await pilot.pause()


async def test_jumper_binding_exists(test_app):
    """Test that ctrl+o binding exists for show_jumper"""
    async with test_app.run_test(size=APP_SIZE) as pilot:
        # Check that the binding exists
        bindings = {binding.key: binding.action for binding in pilot.app.BINDINGS}
        assert "ctrl+o" in bindings
        assert bindings["ctrl+o"] == "show_jumper"


async def test_interaction_buttons_have_jump_mode(test_app):
    """Test that interaction panel buttons have jump_mode set"""
    async with test_app.run_test(size=APP_SIZE) as pilot:
        # Test main action buttons
        btn_shell_export = pilot.app.query_one("#btn-shell-export", Button)
        assert hasattr(btn_shell_export, "jump_mode")
        assert btn_shell_export.jump_mode == "click"

        btn_file_export = pilot.app.query_one("#btn-file-export", Button)
        assert hasattr(btn_file_export, "jump_mode")
        assert btn_file_export.jump_mode == "click"

        btn_copy_path = pilot.app.query_one("#btn-copy-path", Button)
        assert hasattr(btn_copy_path, "jump_mode")
        assert btn_copy_path.jump_mode == "click"

        btn_shell_select = pilot.app.query_one("#btn-shell-select", Button)
        assert hasattr(btn_shell_select, "jump_mode")
        assert btn_shell_select.jump_mode == "click"

        btn_new_file = pilot.app.query_one("#btn-new-file", Button)
        assert hasattr(btn_new_file, "jump_mode")
        assert btn_new_file.jump_mode == "click"

        btn_save_file = pilot.app.query_one("#btn-save-file", Button)
        assert hasattr(btn_save_file, "jump_mode")
        assert btn_save_file.jump_mode == "click"


async def test_filepanel_buttons_have_jump_mode(test_app, test_data_path):
    """Test that file panel edit/delete buttons have jump_mode set"""
    # Create a test file
    (test_data_path / "testfile.env").touch()

    async with test_app.run_test(size=APP_SIZE) as pilot:
        # Wait for UI to update
        await pilot.pause()

        # Query all edit and delete buttons
        edit_buttons = pilot.app.query(".edit")
        delete_buttons = pilot.app.query(".delete")

        # Check that at least one of each exists
        assert len(edit_buttons) > 0, "No edit buttons found"
        assert len(delete_buttons) > 0, "No delete buttons found"

        # Check that all edit buttons have jump_mode set
        for btn in edit_buttons:
            assert hasattr(btn, "jump_mode"), f"Button {btn.id} missing jump_mode"
            assert btn.jump_mode == "click", f"Button {btn.id} has wrong jump_mode"

        # Check that all delete buttons have jump_mode set
        for btn in delete_buttons:
            assert hasattr(btn, "jump_mode"), f"Button {btn.id} missing jump_mode"
            assert btn.jump_mode == "click", f"Button {btn.id} has wrong jump_mode"


async def test_collapsible_has_jump_mode(test_app, test_data_path):
    """Test that Collapsible folders have jump_mode set"""
    # Create test files in folders
    (test_data_path / "folder1").mkdir()
    (test_data_path / "folder1" / "file1.env").touch()
    (test_data_path / "folder2").mkdir()
    (test_data_path / "folder2" / "file2.env").touch()

    async with test_app.run_test(size=APP_SIZE) as pilot:
        await pilot.pause()

        # Query all collapsible widgets
        from dotenvhub.widgets.filepanel import CustomCollapsible

        collapsibles = pilot.app.query(CustomCollapsible)

        # Check that at least one exists
        assert len(collapsibles) > 0, "No collapsible folders found"

        # Check that all collapsibles have jump_mode set
        for collapsible in collapsibles:
            assert hasattr(collapsible, "jump_mode"), (
                f"Collapsible {collapsible.title} missing jump_mode"
            )
            assert collapsible.jump_mode == "click", (
                f"Collapsible {collapsible.title} has wrong jump_mode"
            )


async def test_jumper_can_be_triggered_with_keybind(test_app):
    """Test that jumper overlay can be triggered with ctrl+o"""
    async with test_app.run_test(size=APP_SIZE) as pilot:
        jumper = pilot.app.query_one(Jumper)
        assert jumper is not None

        # Press ctrl+o to show jumper (should not raise an error)
        await pilot.press("ctrl+o")
        await pilot.pause()
