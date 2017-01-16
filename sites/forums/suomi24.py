# -*- coding: utf-8 -*-

import os.path, sys
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import processor

def parse( url ):

	r = requests.get( url )
	if r.status_code == 404:
		return {}

	r.encoding = 'UTF-8'
	soup = BeautifulSoup( r.text, "html.parser" )

	thread = soup.find( class_ = 'thread')
	info = thread.find( class_ = 'user-info-big' )
	breadcrumbs = []
	for li in thread.find( class_ = 'breadcrumb' ).find_all( 'li' ):
		breadcrumbs.append( processor.collect_text( li ) )

	title = breadcrumbs[-1]
	topics = breadcrumbs[1:-1]
	user = processor.collect_text( info.find( class_ = 'user-info-name' ) )
	user_role = processor.collect_text( info.find( class_ = 'user-info-role' ) )
	time = processor.collect_datetime( info.find( class_ = 'user-info-timestamp' ) )[0]
	text = processor.collect_text( thread.find( class_ = 'thread-text' ) )
	answers = get_answers( thread.find_all( class_ = 'answer-block-container' ), user )

	return {'title' : title,
			'topics' : topics,
			'user' : user,
			'user_role' : user_role,
			'time' : time,
			'text' : text,
			'answers' : answers}

def get_answers( answers_html_element, to_user ):
	answers = []

	for answer in answers_html_element:
		answer_data = {}
		answer_div = answer.find( class_ = 'answer-container' )

		answer_data['likes'] = processor.collect_text( answer_div.find( class_ = 'action-bar-vote-count') )
		processor.decompose( answer_div.find( class_ = 'action-bar' ) )

		answer_data['user'] = processor.collect_text( answer_div.find( class_ = 'user-info-name') )
		answer_data['user_role'] = processor.collect_text( answer_div.find( class_ = 'user-info-role') )
		answer_data['time'] = processor.collect_datetime( answer_div.find( class_ = 'user-info-timestamp') )[0]
		answer_data['text'] = processor.collect_text( answer_div.find( class_ = 'answer') )
		answer_data['to'] = to_user
		answer_data['comments'] = get_comments( answer.find( class_ = 'comments' ), answer_data['user'] )
		answers.append(answer_data)

	return answers

def get_comments( comments_html_element, to_user ):
	comments = []

	comments_list = comments_html_element.find( class_ = 'comments-list' )

	if comments_list:

		for comment_div in comments_list.find_all( class_ = 'comment' ):
			comment_data = {}

			comment_data['likes'] = processor.collect_text( comment_div.find( class_ = 'action-bar-vote-count') )
			processor.decompose( comment_div.find( class_ = 'action-bar' ) )

			comment_data['user'] = processor.collect_text( comment_div.find( class_ = 'user-info-name') )
			comment_data['user_role'] = processor.collect_text( comment_div.find( class_ = 'user-info-role') )
			comment_data['time'] = processor.collect_datetime( comment_div.find( class_ = 'user-info-timestamp') )[0]
			comment_data['text'] = processor.collect_text( comment_div.find( class_ = 'comment-text') )
			comment_data['to'] = to_user
			comment_data['quote'] = {}

			blockquote = comment_div.find( 'blockquote' )
			if blockquote:
				comment_data['quote']['from'] = processor.collect_text( blockquote.find( 'header' ).find( 'strong' ) )
				comment_data['quote']['text'] = processor.collect_text( blockquote.find( class_ = 'text-muted blockquote-collapse-body' ) )

			comments.append(comment_data)

	return comments


if __name__ == '__main__':
	parse("http://keskustelu.suomi24.fi/t/14671537/sioille-helmia")
