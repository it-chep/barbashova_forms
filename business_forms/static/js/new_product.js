$(document).ready(function () {
    const $form = $('form');

    function getContainer($field) {
        return $field.closest('.field_inline_item_container');
    }

    function showError($container, message) {
        $container.addClass('invalid');
        $container.find('.line').addClass('invalid');
        $container.find('.field_item_warning_container').show();
        if (message) {
            $container.find('.warning_text').html(message);
        }
    }

    function clearError($container) {
        $container.removeClass('invalid');
        $container.find('.line').removeClass('invalid');
        $container.find('.field_item_warning_container').hide();
        $container.find('.warning_text').text('Это обязательный вопрос.');
    }

    function autoResize($textarea) {
        $textarea.css('height', 'auto');
        $textarea.css('height', $textarea[0].scrollHeight + 'px');
    }

    function syncOtherInputState() {
        const enabled = $('input[name="mri_experience"]:checked').val() === 'other';
        const $otherInput = $('#id_mri_experience_other');
        const $otherContainer = $('#mri-experience-other-container');
        $otherInput.prop('disabled', !enabled);
        $otherContainer.toggle(enabled);
        if (!enabled) {
            $otherInput.val('');
            clearError(getContainer($otherInput));
        }
    }

    function syncDescriptionDetailsState() {
        const enabled = $('input[name="mri_description_experience"]:checked').val() === 'yes';
        const $detailsInput = $('#id_mri_description_experience_details');
        const $detailsContainer = $('#mri-description-details-container');
        $detailsInput.prop('disabled', !enabled);
        $detailsContainer.toggle(enabled);
        if (!enabled) {
            $detailsInput.val('');
            clearError(getContainer($detailsInput));
        }
    }

    $('.auto-resize-textarea').each(function () {
        const $textarea = $(this);
        autoResize($textarea);
        $textarea.on('input', function () {
            autoResize($(this));
        });
    });

    $('input, textarea').on('input change blur', function () {
        clearError(getContainer($(this)));
    });

    $('#radio').on('click', function () {
        $('#id_policy_agreement').prop('checked', true);
        clearError(getContainer($('#id_policy_agreement')));
    });

    $('input[name="mri_experience"]').on('change', syncOtherInputState);
    $('input[name="mri_description_experience"]').on('change', syncDescriptionDetailsState);
    syncOtherInputState();
    syncDescriptionDetailsState();

    $('.submit_button').on('click', function (e) {
        e.preventDefault();

        const $button = $(this);
        let isValid = true;

        $button.css({opacity: '0.7', 'pointer-events': 'none'});
        $button.find('.submit_text').text('Отправка...');

        ['source', 'mri_experience', 'specialization', 'work_schedule'].forEach(function (fieldName) {
            const $field = $(`input[name="${fieldName}"]`);
            if (!$field.is(':checked')) {
                showError(getContainer($field.first()));
                isValid = false;
            }
        });

        if ($('input[name="mri_experience"]:checked').val() === 'other' && !$('#id_mri_experience_other').val().trim()) {
            showError(getContainer($('#id_mri_experience_other')));
            isValid = false;
        }

        const $mriDescriptionExperience = $('input[name="mri_description_experience"]');
        if (!$mriDescriptionExperience.is(':checked')) {
            showError(getContainer($mriDescriptionExperience.first()));
            isValid = false;
        }
        if ($('input[name="mri_description_experience"]:checked').val() === 'yes' && !$('#id_mri_description_experience_details').val().trim()) {
            showError(getContainer($('#id_mri_description_experience_details')));
            isValid = false;
        }

        ['city', 'income_rub', 'difficult_sections', 'can_plan_mri', 'convenient_time', 'convenient_weekdays', 'full_name', 'phone', 'telegram'].forEach(function (fieldName) {
            const $field = $(`[name="${fieldName}"]`);
            if (!$field.val().trim()) {
                showError(getContainer($field));
                isValid = false;
            }
        });

        if (!$('#id_policy_agreement').prop('checked')) {
            showError(getContainer($('#id_policy_agreement')));
            isValid = false;
        }

        if (!isValid) {
            resetButtonState($button);
            return;
        }

        $.ajax({
            type: 'POST',
            url: $form.attr('action'),
            data: $form.serialize(),
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    window.location.href = response.redirect_url;
                    return;
                }

                $.each(response.errors || {}, function (fieldName, messages) {
                    const $field = $(`[name="${fieldName}"]`);
                    showError(getContainer($field.first().length ? $field.first() : $('#id_' + fieldName)), messages.join('<br>'));
                });

                resetButtonState($button);
            },
            error: function () {
                resetButtonState($button);
            }
        });
    });

    function resetButtonState($button) {
        $button.css({opacity: '1', 'pointer-events': 'auto'});
        $button.find('.submit_text').text('Отправить');
    }

    $('.clear_inline_container').on('click', function () {
        $form[0].reset();
        $('.field_inline_item_container').each(function () {
            clearError($(this));
        });
        $('#id_policy_agreement').prop('checked', false);
        syncOtherInputState();
        syncDescriptionDetailsState();
    });
});
