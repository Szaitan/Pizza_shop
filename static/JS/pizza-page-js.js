$(document).ready(function() {
    // Initialize selected options and initialCost
    var selectedOptions = {
        size: "",
        dough: "",
        cheese: ""
    };

    var initialCost = parseFloat($("#pizza_cost").text());

    // Initialize the number of pizzas
    var numberOfPizzas = 1;

    // Function to update the pizza cost based on selected options and number of pizzas
    function updateCost() {
        var totalCost = initialCost;

        // Add the selected size cost
        if (selectedOptions.size !== "") {
            totalCost += parseFloat(selectedOptions.size.attr("data-price"));
        }

        // Add the selected dough cost
        if (selectedOptions.dough !== "") {
            totalCost += parseFloat(selectedOptions.dough.attr("data-price"));
        }

        // Add the selected cheese cost
        if (selectedOptions.cheese !== "") {
            totalCost += parseFloat(selectedOptions.cheese.attr("data-price"));
        }

        // Multiply the total cost by the number of pizzas
        totalCost *= numberOfPizzas;

        // Update the hidden input field value
        $("#total_pizza_cost").val(totalCost);

        $("#pizza_cost").text(totalCost);
    }

    // Button click event handler for size, dough, and cheese options
    $(".size-option, .dough-option, .cheese-option").click(function() {
        var optionType = $(this).attr("data-option");

        // Remove active class from all options of the same type
        $("." + optionType + "-option").removeClass("active");

        // Apply active class to the clicked option
        $(this).addClass("active");

        // Update the selected option
        selectedOptions[optionType] = $(this);

        // Update the pizza cost
        updateCost();
    });

    // Button click event handler for incrementing the number of pizzas
    $(".size-buttons.increment").click(function() {
        numberOfPizzas++;
        $("#number").text(numberOfPizzas);

        // Update the pizza cost
        updateCost();
    });

    // Button click event handler for decrementing the number of pizzas
    $(".size-buttons.decrement").click(function() {
        if (numberOfPizzas > 1) {
            numberOfPizzas--;
            $("#number").text(numberOfPizzas);

            // Update the pizza cost
            updateCost();
        }
    });
});
