๓
๕ฮjYc           @@ s   d  d l  m Z d  d l  m Z d  d l Z d  d l Td  d l Td  d l Td  d l Td  d l j	 Z
 d  d l m Z d Z d Z e d d d d d	 d
  Z d S(   i    (   t   print_function(   t   absolute_importN(   t   *(   t   _obtain_input_shapes=   /media/linkwong/D/vgg19_weights_tf_dim_ordering_tf_kernels.h5sy   https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5t   imageneti่  c      
   C@ sึ  | d dB h k r! t d   n  | d k rN |  rN | d k rN t d   n  t | d d d d d	 t j   d
 |  } | dB k r t d |  } n- t j |  sฝ t d | d |  } n | } t d dC d d d d d d |  } t d dD d d d d d d |  } t dE d dF d d |  } t d dG d d d d d d |  } t d dH d d d d d d |  } t dI d dJ d d |  } t d dK d d d d d d |  } t d dL d d d d d d |  } t d dM d d d d d d  |  } t d dN d d d d d d! |  } t dO d dP d d" |  } t d# dQ d d d d d d$ |  } t d# dR d d d d d d% |  } t d# dS d d d d d d& |  } t d# dT d d d d d d' |  } t dU d dV d d( |  } t d# dW d d d d d d) |  } t d# dX d d d d d d* |  } t d# dY d d d d d d+ |  } t d# dZ d d d d d d, |  } t d[ d d\ d d- |  } |  ret	 d d.  |  } t
 d/  |  } t d]  |  } t
 d1 d d d d2 |  } t
 d1 d d d d3 |  } t
 | d d4 d d5 |  } n< | d6 k rt   |  } n | d7 k rกt   |  } n  | dB k	 rผt |  }	 n | }	 t |	 d8 | d d9 }
 t |	 d8 | } | d k rา|  rd: } n t d; t d< d= } |
 j |  t j   d> k rKt j |
  n  t j   d? k rา|  rช|
 j d d-  } | j d0 } |
 j d d2  } t j | | d?  n  t j   d@ k rฯt j dA  qฯqาn  | S(^   sd  Instantiates the VGG19 architecture.
    Optionally loads weights pre-trained
    on ImageNet. Note that when using TensorFlow,
    for best performance you should set
    `image_data_format="channels_last"` in your Keras config
    at ~/.keras/keras.json.
    The model and the weights are compatible with both
    TensorFlow and Theano. The data format
    convention used by the model is the one
    specified in your Keras config file.
    # Arguments
        include_top: whether to include the 3 fully-connected
            layers at the top of the network.
        weights: one of `None` (random initialization)
            or "imagenet" (pre-training on ImageNet).
        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)
            to use as image input for the model.
        input_shape: optional shape tuple, only to be specified
            if `include_top` is False (otherwise the input shape
            has to be `(224, 224, 3)` (with `channels_last` data format)
            or `(3, 224, 224)` (with `channels_first` data format).
            It should have exactly 3 inputs channels,
            and width and height should be no smaller than 48.
            E.g. `(200, 200, 3)` would be one valid value.
        pooling: Optional pooling mode for feature extraction
            when `include_top` is `False`.
            - `None` means that the output of the model will be
                the 4D tensor output of the
                last convolutional layer.
            - `avg` means that global average pooling
                will be applied to the output of the
                last convolutional layer, and thus
                the output of the model will be a 2D tensor.
            - `max` means that global max pooling will
                be applied.
        classes: optional number of classes to classify images
            into, only to be specified if `include_top` is True, and
            if no `weights` argument is specified.
    # Returns
        A Keras model instance.
    # Raises
        ValueError: in case of invalid argument for `weights`,
            or invalid input shape.
    R   sp   The `weights` argument should be either `None` (random initialization) or `imagenet` (pre-training on ImageNet).i่  sS   If using `weights` as imagenet with `include_top` as true, `classes` should be 1000t   default_sizeiเ   t   min_sizei0   t   data_formatt   include_topt   shapet   tensori@   i   t
   activationt   relut   paddingt   samet   namet   block1_conv1t   block1_conv2i   t   stridest   block1_pooli   t   block2_conv1t   block2_conv2t   block2_pooli   t   block3_conv1t   block3_conv2t   block3_conv3t   block3_conv4t   block3_pooli   t   block4_conv1t   block4_conv2t   block4_conv3t   block4_conv4t   block4_poolt   block5_conv1t   block5_conv2t   block5_conv3t   block5_conv4t   block5_poolt   flatteni   i   i   t   fc1t   fc2t   softmaxt   predictionst   avgt   maxt   outputst   vgg19s=   /media/linkwong/D/vgg19_weights_tf_dim_ordering_tf_kernels.h5s1   vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5t   cache_subdirt   modelst   theanot   channels_firstt
   tensorflows๒   You are using the TensorFlow backend, yet you are using the Theano image data format convention (`image_data_format="channels_first"`). For best performance, set `image_data_format="channels_last"` in your Keras config at ~/.keras/keras.json.N(   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   (   i   i   i   (   t   Nonet
   ValueErrorR   t   Kt   image_data_formatt   Inputt   is_keras_tensort   Conv2Dt   MaxPooling2Dt   Flattent   Denset   Reshapet   GlobalAveragePooling2Dt   GlobalMaxPooling2Dt   get_source_inputst   Modelt   get_filet   WEIGHTS_PATH_NO_TOPt   load_weightst   backendt   layer_utilst   convert_all_kernels_in_modelt	   get_layert   output_shapet!   convert_dense_weights_data_formatt   warningst   warn(   R   t   weightst   input_tensort   input_shapet   poolingt   classest	   img_inputt   xt   outputt   inputst   modelt   output_modelt   weights_patht   maxpoolR	   t   dense(    (    s%   /home/linkwong/Desktop/keras_vgg19.pyt   VGG19   s    0		''''''''''''''''!		(   t
   __future__R    R   RL   t   keras.modelst   keras.layerst   keras.enginet   keras.utilst   keras.backendRF   R6   t!   keras.applications.imagenet_utilsR   t   WEIGHTS_PATHRD   t   TrueR4   R\   (    (    (    s%   /home/linkwong/Desktop/keras_vgg19.pyt   <module>   s   



