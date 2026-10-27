/* Trip price calculator + WhatsApp booking link. Reads its settings from data- attributes on #lavigo-calc. */
(function () {
  var root = document.getElementById('lavigo-calc');
  if (!root) return;
  var d = root.dataset;
  var priceAdult = +d.adult, priceChild = +d.child, cur = d.currency;
  var dateSel = root.querySelector('[name="date"]');
  var inputs = { adults: root.querySelector('[name="adults"]'), children: root.querySelector('[name="children"]'), infants: root.querySelector('[name="infants"]') };
  var mins = { adults: 1, children: 0, infants: 0 };
  var btn = root.querySelector('.lavigo-wa-btn');

  function money(n) { return cur + n.toLocaleString('en-IN'); }
  function val(k) { if (!inputs[k]) return 0; var v = parseInt(inputs[k].value, 10); return isNaN(v) ? mins[k] : Math.max(mins[k], Math.min(20, v)); }
  function out(k, txt) { var el = root.querySelector('[data-out="' + k + '"]'); if (el) el.textContent = txt; }

  function update() {
    var a = val('adults'), c = val('children'), i = val('infants');
    var ta = a * priceAdult, tc = c * priceChild, total = ta + tc;
    out('adults', a + ' × ' + money(priceAdult));
    out('adults-total', money(ta));
    out('children', c + ' × ' + money(priceChild));
    out('children-total', money(tc));
    out('infants', i);
    out('total', money(total));
    var date = dateSel.options[dateSel.selectedIndex].text;
    var msg = 'Hello ' + d.company + ', I would like to book this trip:\n\n' +
      '*' + d.trip + '* (' + d.days + ')\n' +
      'Date: ' + date + '\n' +
      (inputs.children ? 'Adults (above 10 years): ' : 'Travellers: ') + a + ' x ' + money(priceAdult) + '\n' +
      (inputs.children ? 'Children (3-10 years): ' + c + ' x ' + money(priceChild) + '\n' : '') +
      (i ? 'Children under 3: ' + i + ' (free)\n' : '') +
      'Estimated total: ' + money(total) + '\n\n' +
      'Page: ' + location.href;
    btn.href = 'https://wa.me/' + d.wa + '?text=' + encodeURIComponent(msg);
  }

  root.querySelectorAll('[data-step]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault();
      var k = b.getAttribute('data-for');
      inputs[k].value = Math.max(mins[k], Math.min(20, val(k) + (+b.getAttribute('data-step'))));
      update();
    });
  });
  Object.keys(inputs).forEach(function (k) { if (!inputs[k]) return; inputs[k].addEventListener('input', update); inputs[k].addEventListener('change', function () { inputs[k].value = val(k); update(); }); });
  dateSel.addEventListener('change', update);
  root.querySelector('form').addEventListener('submit', function (e) { e.preventDefault(); });
  update();
})();
