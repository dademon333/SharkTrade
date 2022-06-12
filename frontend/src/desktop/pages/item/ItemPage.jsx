import {connect} from 'react-redux';
import {useParams} from 'react-router-dom';
import {useEffect} from 'react';

import Template from '../../template/Template';
import RestAPI from '../../../RestAPI';
import TextFunctions from '../../../TextFunctions';
import Page404 from '../page404/Page404';
import LoadingSpinnerPage from '../../components/LoadingSpinnerPage';
import LinkButton from '../../components/LinkButton';
import {modalChanged} from '../../../slices/Global';
import {itemPageItemDataChanged} from '../../../slices/Content';

import './ItemPage.scss';
import {ReactComponent as Article} from '../../../icons/article.svg';


const withTemplate = (content) => (
    <Template className={'item-page'}>
        {content}
    </Template>
)


const ItemPage = (props) => {
    let {id: itemId} = useParams();
    itemId = parseInt(itemId);

    const {itemPageItemDataChanged} = props;
    const item = props.content.itemPageItemsData[itemId];

    useEffect(() => {
        const getItem = async () => {
            const item = await RestAPI.getItem(itemId);
            itemPageItemDataChanged({itemId, item});
        }

        if (item === undefined && TextFunctions.isNatural(itemId)) {
            getItem().then();
        }
    });

    if (!TextFunctions.isNatural(itemId)) {
        return <Page404/>
    }

    if (item === undefined) {
        return withTemplate(<LoadingSpinnerPage />)
    }

    if (item.detail) {
        return <Page404/>
    }

    const {
        name,
        description,
        photo_url: photoUrl
    } = item;

    return withTemplate(
        <>
            <div className="left-part">
                <img src={photoUrl} alt="фото" />
                <LinkButton to="/storage">Назад в склад</LinkButton>
            </div>
            <div className="right-part">
                <div className="name">{name}</div>
                <div className="description frame">
                    <div className="description__header">
                        <Article />
                        Описание
                    </div>
                    <div className="description__text">
                        {description}
                    </div>
                </div>
            </div>
        </>
    )
}


const mapStateToProps = (state) => ({
    user: state.user,
    content: state.content
});

const mapDispatchToProps = {
    modalChanged,
    itemPageItemDataChanged
}

export default connect(mapStateToProps, mapDispatchToProps)(ItemPage);