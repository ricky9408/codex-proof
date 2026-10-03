const before = new URLSearchParams(location.search).get('variant') === 'before';
const {totalCents, removeItem} = await import(before ? './cart.buggy.mjs' : './cart.mjs');
const catalog = {notebook:{id:'notebook',name:'Notebook',priceCents:1200},mug:{id:'mug',name:'Ceramic mug',priceCents:1800}};
let items=[], total=0;
const money = value => '$'+(value/100).toFixed(2);
document.querySelector('#variant').textContent = before ? 'Before fix' : 'After fix';
function render(){
  const container=document.querySelector('#items'); container.replaceChildren();
  if(!items.length){const p=document.createElement('p');p.className='empty';p.textContent='Add an item to reproduce the report.';container.append(p);}
  items.forEach(item=>{const row=document.createElement('div');row.className='item';const label=document.createElement('div');label.textContent=item.name;const price=document.createElement('small');price.textContent=money(item.priceCents);label.append(price);const button=document.createElement('button');button.textContent='Remove';button.setAttribute('aria-label','Remove '+item.name);button.addEventListener('click',()=>{const result=removeItem(items,item.id);items=result.items;total=result.totalCents;render();});row.append(label,button);container.append(row);});
  document.querySelector('#total').textContent=money(total);
}
for(const id of Object.keys(catalog))document.querySelector('#add-'+id).addEventListener('click',()=>{if(!items.some(item=>item.id===id))items.push(catalog[id]);total=totalCents(items);render();});
document.querySelector('#reset').addEventListener('click',()=>{items=[];total=0;render();});render();
