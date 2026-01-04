(function () {
    const addBtn = document.getElementById("add-ingredient-btn");
    const container = document.getElementById("ingredients-container");
    const template = document.getElementById("ingredient-empty-form-template");

    const totalFormsInput = document.getElementById("id_ingredients-TOTAL_FORMS");

    if (!addBtn || !container || !template || !totalFormsInput) return;

    addBtn.addEventListener("click", () => {
      const formIndex = parseInt(totalFormsInput.value, 10);

      const html = template.innerHTML.replaceAll("__prefix__", formIndex);

      container.insertAdjacentHTML("beforeend", html);

      totalFormsInput.value = formIndex + 1;
    });
})();