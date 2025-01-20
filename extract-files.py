#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.fixups_lib import (
    lib_fixup_vendorcompat,
    lib_fixups,
    lib_fixups_user_type,
)

namespace_imports = [
    'hardware/xiaomi',
    'vendor/qcom/opensource/display',
    'vendor/xiaomi/sm8250-common',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'proprietary/vendor/lib64/libcamxncs.so',
        'proprietary/vendor/lib64/sensors.touch.so',
    ): lib_fixup_vendorcompat,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/init/init.batterysecret.rc': blob_fixup()
        .regex_replace('\\s*seclabel u:r:batterysecret:s0', ''),
    'vendor/lib/hw/audio.primary.cmi.so': blob_fixup()
        .binary_regex_replace(b'/vendor/lib/liba2dpoffload.so', b'liba2dpoffload_cmi.so\x00\x00\x00\x00\x00\x00\x00\x00'),
    'vendor/lib64/camera/components/com.mi.node.watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    'vendor/lib64/vendor.qti.hardware.camera.postproc@1.0-service-impl.so': blob_fixup()
        .sig_replace('9A 0A 00 94', '1F 20 03 D5'),
}  # fmt: skip

module = ExtractUtilsModule(
    'cmi',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'sm8250-common', module.vendor)
    utils.run()
