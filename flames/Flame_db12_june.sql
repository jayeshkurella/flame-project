PGDMP                         {            FLAME_DB    12.10    12.10     �
           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                        0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    177347    FLAME_DB    DATABASE     �   CREATE DATABASE "FLAME_DB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE "FLAME_DB";
                postgres    false            �            1259    177366    data    TABLE     �  CREATE TABLE public.data (
    major character varying(512),
    submajor character varying(512),
    minor character varying(512),
    subminor character varying(512),
    grade character varying(512),
    file_formats text,
    type character varying(512),
    source_description character varying(512),
    place_city character varying(512),
    year character varying(512),
    publisher character varying(512),
    path character varying(512),
    collection character varying(512),
    collection_type character varying(512),
    soi_toposheet_no character varying(512),
    grade1 character varying(512),
    data_resolution character varying(512),
    ownership character varying(512),
    is_processed character varying(512),
    short_descr character varying(512),
    descr text,
    img_service text,
    img_dw character varying(512),
    map_service character varying(512),
    map_dw character varying(512),
    publish_on character varying(512),
    thumbnail text
);
    DROP TABLE public.data;
       public         heap    postgres    false            �
          0    177366    data 
   TABLE DATA           H  COPY public.data (major, submajor, minor, subminor, grade, file_formats, type, source_description, place_city, year, publisher, path, collection, collection_type, soi_toposheet_no, grade1, data_resolution, ownership, is_processed, short_descr, descr, img_service, img_dw, map_service, map_dw, publish_on, thumbnail) FROM stdin;
    public          postgres    false    202   �	       �
   �
  x��\Ys�:~v�
=�TMG����`w��6@:uo�*J�N��-������`��e[�}!:��tt6�rFd��P�y�n0&��Fah=[KD,�մ	1
����Y����@��� k�������/���7��X8��=U���Lq��חQE"���,�ge�Tc���[BPU�T�1��*|$�{�^+O=j�=@�
��W>�k�`B����*�H�mN`�	,�QP��4�˧@v,�	ց�N6ߜ���ӥ���/�'^R0M���o-9�򞫄\�	��}�n�3�/f�oIZ�˪��9}�4�� �5��G�j8Գ�5�@�DI5����r�fQoA��������Dձ"~-wP�_o	r����嬵Lʟ��N3�z��l�^�^��c��s���J���!�>�����K���ߵ�m@HT���m�Y�URL1Y�̴:3�$.Tm�n�*�j��*&U��%�Tl���=ЅX��^�W"yZ}����UYł�!�]���{V��IhЪ^Ƃ'!�l��R��,�5��NFre���{�;I*��a���t^[+//L����͠��D�wFé��L�U��!�T*L��q���;�QK������N���6���zï`�A��&�:�"m����\�10'�I�[�J�����)��H��c�<U���1����QoȌ|s}.w��(H?�HB���}�c��L�wy�Iz��}B��y$����2�7aT�,�O,U^l]�F.˷���#�� ��2���)�qG�'��0΃��!��c�kW�c4����n��˥�5x'ٰy$�w���R"���M�hך���?hԶ�A˶�k��j_W!�j��K朐8�b����}*Ç��ͮ,�U�B6�X���Qo�n�����9jS>����@��c{�8 [ߧ���S3H�a)q9��&�R�*De%�?b�4Ed!�94戥�=�B�D}�P�%24.���rW�t߬�sY��ě�lG����pf�����Nʀ%S�r\�©�u޾������x[�-a�w�W�� �V܇ŕ�T����s'q�3�r���$��.��k>
��;`c���w�Ҭ��8d$^�}F�]r#W�{�
�\�m��浍;`�4dN�8�,�dUz��l��%�G���3[���%?�¶�L�I�Od���m�Ke��w�k��\����&<A/��������Օ���m wB��&����
P�/��������/�9D�֨$�d�V�*9W���}���Nī�4uc�}Ձv��敼s,�*��Q%XjR�����Fà�(mx�o��h��f�b04�o�H�#���e��� �q˛�hTㅥe�An]�c""i���`���	ld#�(\���`N���+{�b�O�(�?�KO�p<%gi�s�"�<"RS��Ҙ�Qo���G��Pa�R�	�	�IW�%���l���j�����|��Oz�E���B'O)�b�8�pJlI�����I5E��2g@��r'U ��e��`���`r�Xhu�A͚�^!c�rWk��vP����.�0����zD	hzᢖ{�Bǻ��hT-�L>{@�Ʊ���Ԏ�D��e��Ǎ2i%g�����R�W!��C4͞�K2�W�yb��G��Kw.Qn�"�X��2<��W
��;cp�%؄�W��{4��;���v{C�z���cW@�EO�N}���x�u����j*�'\YS���ʚ��Σ�4	�σ�|��Ȕ����3���+pu~��B�U7�0�|M}�jz��6�{��q ����F:��)Wo�����nN�a�4d&�cGD�]n�#ʃ��
�(��U�Wu Yu��JWQ*���"�%���D�6�e���������C����n�H�C~^�}�n����"�ѓ7�;�H�:���������ZB�v�mV��hBV9�x��r���7��3����CuSD�MMERW}C�z�Flmb�4א ٚ�?i����8��z�t!�a�jdTC}:6;�:4��}�u��/`;p|D9�����hl�!4�=+"aL��P�7�a������ #���ghe�궙ML} F�<:l-CIK̂<��?\ȡO	��<�F[�o	���1��񚾇��.�8���[����ٲH�.3��9�6:��&c���wX�)�.�@���ׇ�T�݀����K����j,�R���Q��i�G�b4ar��ďW-[��X�OO(X�1�o�,���B��=�~��� 8�y��ۢ��n�ϡu��S�᜗ۮ G�TbA$��8�~�k}<�E9��]Ǵnc��&�7�.�+eG��&�:,�����1�4�sji�Q����D�S��Z�#�\Ґi���^M����|#g������/%�m�B<�n#C�C� �*a��)�Q�M��g� <kG�dО�j��U��7DY�.�֨���=4
��&~_9�6e����l�"%|���r��%����t'@l�5;7�`P,$��#tw��ay��C�b�I�~e��&2�Qg������\Y���I�hk8@,*�\y:"R�׎`#Đ'����*:7
7U�^�lmH=;�t�J���SC�m9��0$Tw���X}�����j�_{�s8���V�%ա�^:�7��+�F�{qK)� R7��^�kxoeu�n|��_�nDߨ�+J=�d ����ZS��;o4��|3�z������_g_�|��ʆD     