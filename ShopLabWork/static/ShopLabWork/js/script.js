//counter product
let count_input = document.getElementById('count-input')

let plus_button = document.getElementById('button-plus')

plus_button.onclick = function(){
  count_input.setAttribute('value', Number(count_input.getAttribute('value'))+1)
};

let minus_button = document.getElementById('button-minus')

minus_button.onclick = function(){
  count_input.setAttribute('value', Math.max(Number(count_input.getAttribute('value')) - 1, 1))
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