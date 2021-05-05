from odoo.addons.component.core import Component

class EdiBookListenerOutput(Component):
    _name = "edi.book.listener.output"
    _inherit = "base.event.listener"
    _apply_on = ["library.book", "library.book.wizard"]

    def _get_book_backend(self, record):
        return record.env.ref("my_library.book_backend")

    def _get_backend(self, record):
        return self._get_book_backend(record)

    def _get_exchange_record_vals(self, record):
        return {"model": record._name, "res_id": record.id}

    def on_post_book_title(self, record):
        backend = self._get_backend(record)
        exchange_type = "book_title"
        exchange_record = backend.create_record(exchange_type, self._get_exchange_record_vals(record))
        backend.generate_output(exchange_record)
        backend.exchange_send(exchange_record)


