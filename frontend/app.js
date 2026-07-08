const API_BASES = ["http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1:8001"];
const AUTO_REFRESH_MS = 10000;
let activeApiBase = localStorage.getItem("uptime_api_base") || API_BASES[0];

async function apiFetch(path, options){
  const bases = [activeApiBase, ...API_BASES].filter((base, index, arr) => arr.indexOf(base) === index);
  let lastError;

  for(const base of bases){
    try{
      const res = await fetch(`${base}${path}`, options);
      activeApiBase = base;
      localStorage.setItem("uptime_api_base", base);
      return res;
    }catch(err){
      lastError = err;
    }
  }

  throw lastError || new Error("API request failed");
}

async function fetchUrls(){
  const res = await apiFetch('/urls/');
  if(!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

function formatDateTime(value){
  if(!value) return '-';
  const hasTimeZone = /(?:Z|[+-]\d{2}:?\d{2})$/i.test(value);
  const normalizedValue = hasTimeZone ? value : `${value}Z`;
  return new Date(normalizedValue).toLocaleString();
}

function renderUrls(urls){
  const tbody = document.querySelector('#urls-table tbody');
  tbody.innerHTML = '';
  for(const u of urls){
    const status = u.latest_check
      ? u.latest_check.is_up ? 'UP' : 'DOWN'
      : 'unknown';
    const responseTime = u.latest_check ? `${u.latest_check.response_time_ms} ms` : '-';
    const checkedAt = u.latest_check ? formatDateTime(u.latest_check.checked_at) : '-';
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${u.id}</td>
      <td>${u.url}</td>
      <td>${status}</td>
      <td>${responseTime}</td>
      <td>${checkedAt}</td>
      <td>${formatDateTime(u.created_at)}</td>
    `;
    tbody.appendChild(tr);
  }
}

async function load(){
  try{
    const urls = await fetchUrls();
    renderUrls(urls);
  }catch(e){
    console.error(e);
  }
}

document.addEventListener('DOMContentLoaded', ()=>{
  load();

  document.querySelector('#add-form').addEventListener('submit', async (ev)=>{
    ev.preventDefault();
    const input = document.querySelector('#url-input');
    const value = input.value.trim();
    if(!value) return;
    try{
      const res = await apiFetch('/urls/', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:value})});
      if(!res.ok){
        const err = await res.json();
        alert('Error: '+(err.detail || 'Failed'));
        return;
      }
      input.value='';
      load();
    }catch(err){
      console.error(err);
      alert('Request failed');
    }
  })

  setInterval(load, AUTO_REFRESH_MS);
})
