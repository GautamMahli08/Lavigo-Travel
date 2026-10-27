/* "Plan a custom trip" form: builds a WhatsApp message from the answers. */
(function () {
  var root = document.getElementById('lavigo-custom');
  if (!root) return;
  var form = root.querySelector('form');

  root.querySelectorAll('[data-step]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault();
      var input = form.querySelector('[name="' + b.getAttribute('data-for') + '"]');
      var min = +input.min || 0, max = +input.max || 30;
      input.value = Math.max(min, Math.min(max, (parseInt(input.value, 10) || 0) + (+b.getAttribute('data-step'))));
    });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = function (n) { var el = form.querySelector('[name="' + n + '"]'); return el ? el.value.trim() : ''; };
    if (!f('name')) { form.querySelector('[name="name"]').focus(); return; }
    var places = Array.prototype.map.call(form.querySelectorAll('[name="places"]:checked'), function (c) { return c.value; });
    var month = f('month');
    if (month) {
      var d = new Date(month + '-01T00:00:00');
      if (!isNaN(d)) month = d.toLocaleDateString('en-GB', { month: 'long', year: 'numeric' });
    }
    var lines = [
      'Hello ' + root.dataset.company + ', I would like to plan a custom trip.',
      '',
      'Name: ' + f('name'),
      f('phone') ? 'Phone: ' + f('phone') : '',
      'Places: ' + (places.length ? places.join(', ') : 'Not decided yet'),
      'When: ' + (month || 'Flexible'),
      'Days: ' + f('days'),
      'Adults: ' + f('adults') + ', Children: ' + f('children'),
      'Budget: ' + f('budget'),
      f('message') ? 'Notes: ' + f('message') : ''
    ].filter(function (l, i) { return l !== '' || i === 1; });
    window.open('https://wa.me/' + root.dataset.wa + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
  });
})();
