# LinuxCNC hardware module test

sh_test()
{
	local interpreter="$1"

	cd "$rootdir" || die "Failed to change to rootdir '$rootdir'"

	modpath="$rootdir/fake/linuxcnc_fake_hal"

	PYTHONPATH="$modpath:$PYTHONPATH" \
	JYTHONPATH="$modpath:$JYTHONPATH" \
	IRONPYTHONPATH="$modpath:$IRONPYTHONPATH" \
		"$interpreter" ./awlsim-linuxcnc-hal \
		--check-cnc 0 --onecycle "$rootdir/tests/000-base/empty.awl" ||\
			test_failed "LinuxCNC test failed"
}
