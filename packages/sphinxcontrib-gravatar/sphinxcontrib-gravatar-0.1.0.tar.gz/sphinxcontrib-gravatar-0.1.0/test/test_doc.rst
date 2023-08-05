===============
Acceptance Test
===============

If all element are valid, test is done successfully.

Normal
---------------------------------------------------

source::

 .. gravatar:: tell-k

output:

.. gravatar:: tell-k

Optional Settings
---------------------------------------------------

source::

 .. gravatar:: tell-k
    :size: 200
    :default: mm
    :target: http://github.com/tell-k
    :rating: pg
    :class: test-gravatar
    :alt: altnativetext

output:

.. gravatar:: tell-k
   :size: 200
   :default: mm
   :target: http://github.com/tell-k
   :rating: pg
   :class: test-gravatar
   :alt: altnativetext

Force Default Image
---------------------------------------------------

This option displays the default image forces.

source::

 .. gravatar:: tell-k
    :default: monsterid
    :force_default:


output:

.. gravatar:: tell-k
   :default: monsterid
   :force_default:


Unlink
---------------------------------------------------

This option does not set the URL link to the image.

source::

 .. gravatar:: tell-k
    :unlink:

output:

.. gravatar:: tell-k
   :unlink:

Substitution References
---------------------------------------------------

If you want to embed in-line, please use "Substitution References".

source::

 My Gravagar image is |tell-k-gravatar|. This is the identity on the Internet of me.

 .. |tell-k-gravatar| gravatar:: tell-k
     :size: 100
     :target: http://tell-k.hatenablog.com

output:

My Gravagar image is |tell-k-gravatar|. This is the identity on the Internet of me.

.. |tell-k-gravatar| gravatar:: tell-k
    :size: 100
    :target: http://tell-k.hatenablog.com

