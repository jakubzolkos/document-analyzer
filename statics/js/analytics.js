$(document).ready(function() {

    function updatePlaceholder(mode) {

        var placeholderText = '';
    
        if (mode === 'Dictionary') {
          placeholderText = 'Type the keyword...';
        } else if (mode === 'Documents') {
          placeholderText = 'Type the document name...';
        } else if (mode === 'Paragraphs') {
          placeholderText = 'Type comma separated keywords...';
        }
    
        $('#inp-word').attr('placeholder', placeholderText);
    }

    // Initialize values from localStorage
    const storedMode = localStorage.getItem('mode');
    const storedRange = localStorage.getItem('range');

    if (storedMode) {
        $('#mode-select').val(storedMode);
        updatePlaceholder(storedMode)
    }

    if (storedRange) {
        $('#range-select').val(storedRange);
    }

    // Show or hide range-filter-group based on the mode
    function updateRangeFilterVisibility() {
        const mode = $('#mode-select').val();
        if (mode === 'Paragraphs') {
            $('#range-filter-group').show();
        } else {
            $('#range-filter-group').hide();
        }
    }

    updateRangeFilterVisibility();

    // Event handlers
    $('#mode-select').on('change', function() {
        localStorage.setItem('mode', $(this).val());
        updateRangeFilterVisibility();
        $('#inp-mode').val($(this).val());
        updatePlaceholder($('#mode-select').val());
    });

    $('#range-select').on('change', function() {
        localStorage.setItem('range', $(this).val());
        $('#inp-range').val($(this).val());
    });

    // Set initial hidden input values
    $('#inp-mode').val($('#mode-select').val());
    $('#inp-range').val($('#range-select').val());
});