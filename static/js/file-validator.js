(function ($) {
    "use strict";

    // This set of validators requires the File API, so if we'ere in a browser
    // that isn't sufficiently "HTML5"-y, don't even bother creating them.  It'll
    // do no good, so we just automatically pass those tests.
    var is_supported_browser = !!window.File,
        fileSizeToBytes,
        formatter = $.validator.format;

    /**
     * Converts a measure of data size from a given unit to bytes.
     *
     * @param number size
     *   A measure of data size, in the give unit
     * @param string unit
     *   A unit of data.  Valid inputs are "B", "KB", "MB", "GB", "TB"
     *
     * @return number|bool
     *   The number of bytes in the above size/unit combo.  If an
     *   invalid unit is specified, false is returned
     */
    fileSizeToBytes = (function () {
        var units = ["B", "KB", "MB", "GB", "TB"];
        return function (size, unit) {
            var index_of_unit = units.indexOf(unit),
                converted_size;

            if (index_of_unit === -1) {
                converted_size = false;
            } else {
                while (index_of_unit > 0) {
                    size *= 1024;
                    index_of_unit -= 1;
                }
                converted_size = size;
            }

            return converted_size;
        };
    }());

    /**
     * Validates that an uploaded file is an image, tested by its MIME type.
     *
     * @param obj params
     *   An optional set of configuration parameters. Supported options are:
     *    "types" : array (default ["image"])
     *      An array of file types. The MIME type must start with "image".
     */
    $.validator.addMethod(
        "fileType",
        function (value, element, params) {
            var files,
                types = params.types || ["image"],
                is_valid = false;

            if (!is_supported_browser || this.optional(element)) {
                is_valid = true;
            } else {
                files = element.files;

                if (files.length < 1) {
                    is_valid = false;
                } else {
                    $.each(types, function (key, value) {
                        is_valid = is_valid || files[0].type.indexOf(value) !== -1;
                    });
                }
            }

            return is_valid;
        },
        function (params, element) {
            return formatter(
                "File must be an image of the following types: {0}.",
                params.types.join(", ")
            );
        }
    );

    /**
     * Validates that a file selected for upload is at least a given file size.
     */
    $.validator.addMethod(
        "minFileSize",
        function (value, element, params) {
            var files,
                unit = params.unit || "KB",
                size = params.size || 100,
                min_file_size = fileSizeToBytes(size, unit),
                is_valid = false;

            if (!is_supported_browser || this.optional(element)) {
                is_valid = true;
            } else {
                files = element.files;

                if (files.length < 1) {
                    is_valid = false;
                } else {
                    is_valid = files[0].size >= min_file_size;
                }
            }

            return is_valid;
        },
        function (params, element) {
            return formatter(
                "File must be at least {0}{1} large.",
                [params.size || 100, params.unit || "KB"]
            );
        }
    );

    /**
     * Validates that a file selected for upload is no larger than a given file size.
     */
    $.validator.addMethod(
        "maxFileSize",
        function (value, element, params) {
            var files,
                unit = params.unit || "KB",
                size = params.size || 100,
                max_file_size = fileSizeToBytes(size, unit),
                is_valid = false;

            if (!is_supported_browser || this.optional(element)) {
                is_valid = true;
            } else {
                files = element.files;

                if (files.length < 1) {
                    is_valid = false;
                } else {
                    is_valid = files[0].size <= max_file_size;
                }
            }

            return is_valid;
        },
        function (params, element) {
            return formatter(
                "File cannot be larger than {0}{1}.",
                [params.size || 100, params.unit || "KB"]
            );
        }
    );

}(jQuery));
