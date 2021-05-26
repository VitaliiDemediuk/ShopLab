//Add form
let count_add_form_input = document.getElementById('count-add-form-input')
let size_id_add_form_input = document.getElementById('size_id-add-form-input')

//size select
size_selector = document.getElementById('size_selector')

size_selector.onchange = function () {
  size_id_add_form_input.setAttribute('value', size_selector.options[size_selector.selectedIndex].id)
};


//counter product
let count_input = document.getElementById('count-input')
let plus_button = document.getElementById('button-plus')

plus_button.onclick = function(){
  count_input.setAttribute('value', Number(count_input.getAttribute('value'))+1)
  count_add_form_input.setAttribute('value', count_input.getAttribute('value'))
};

let minus_button = document.getElementById('button-minus')

minus_button.onclick = function(){
  count_input.setAttribute('value', Math.max(Number(count_input.getAttribute('value')) - 1, 1))
  count_add_form_input.setAttribute('value', count_input.getAttribute('value'))
};

//photo picker for detailed product
let product_img_tags = document.getElementById('thumbs-wrap').getElementsByTagName('img')

let img_big_tag = document.getElementById('img-big')

for(let img_tag of product_img_tags){
  img_tag.addEventListener('click', function(){
    img_big_tag.setAttribute('src', img_tag.getAttribute('src'));
    return false;
  });
}