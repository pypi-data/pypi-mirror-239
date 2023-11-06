Usage Sample
''''''''''''

.. code:: python

   from cf import CollFilter

   if __name__ == '__main__':
       data = read_data(train_path)
       data = pre_process(data)  # return [(user_id: str, item_id: str, float),]
       cf = CollFilter(data)
       ucf = cf.user_cf()
       icf = cf.item_cf()


